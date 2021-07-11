import asyncio

from typing import Any, ClassVar, Dict, Optional, Tuple
from urllib.parse import urljoin, urlencode

import aiohttp

from .errors import HTTPException, BadRequest, Unauthorized, Forbidden, NotFound
from .secrets import get_new_code_verifier


class Route:
    BASE: ClassVar[str] = 'https://api.myanimelist.net/'
    FIELDS: ClassVar[str] = 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
    USER_AGENT: ClassVar[str] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.0) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/11.0 Safari/602.1.50'

    def __init__(self, method: str, path: str, version: int = 2, **parameters: Any) -> None:
        self.method = method
        self.path = path
        self.version = version
        self.parameters = parameters
        
        try:
            self.parameters.pop('fields')
            self.parameters['fields'] = self.FIELDS
        except KeyError:
            pass
        
    @property
    def url(self) -> str:
        version = f'v{self.version}'
        base = self.BASE + version
        url = base + self.path + f'?{urlencode(self.parameters)}'
        return url

    @property
    def headers(self) -> Dict[str, str]:
        head = {
            'Content-Type': 'application/json',
            'User-Agent': self.USER_AGENT,
        }
        
        try:
            access_token = self.parameters.pop('access_token')
            head['Authorization'] = f'Bearer {access_token}'
        except KeyError:
            pass

        return head



class HTTPClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.session: Optional[aiohttp.ClientSession] = None

    def generate_auth_url(self) -> Tuple[str, str]:
        code_challenge = get_new_code_verifier()
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.client_id}&code_challenge={code_challenge}'
        return code_challenge, url

    async def request(self, route: Route):
        headers = route.headers
        method = route.method
        url = route.url

        print(url)

        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        for tries in range(5):
            try:
                async with self.session.request(method, url, headers=headers) as response:
                    data = await response.json()

                    if 300 > response.status >= 200:
                        return data
                    
                    # An error occurred
                    error, message = data['error'], data['message']
                    
                    if response.status == 400:
                        raise BadRequest(response, error, message)
                    elif response.status == 401:
                        raise Unauthorized(response, error, message)
                    elif response.status == 403:
                        raise Forbidden(response, error, message)
                    elif response.status == 404:
                        raise NotFound(response, error, message)
                    else:
                        raise HTTPException(response, error, message)
            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in {54, 10054}:
                    await asyncio.sleep(1 + tries * 2)
                    continue

                raise

    async def generate_access_token(self, auth_code: str, code_verifier: str) -> Tuple[str, str]:
        route = Route(
            'POST',
            '/oauth2/token',
            version=1,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=auth_code,
            code_verifier=code_verifier,
            grant_type='authorization_code'
        )

        data = await self.request(route)
        return data['access_token'], data['refresh_token']

    async def get_anime(self, query: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime',
            q=query,
            limit=min(limit, 100),
            offset=offset,
            fields=True,
        )

        return await self.request(route)

    async def get_anime_details(self, anime_id: int):
        route = Route(
            'GET',
            f'/anime/{anime_id}',
            fields=True
        )

        return await self.request(route)

    async def get_anime_ranking(self, ranking_type: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime/ranking',
            ranking_type=ranking_type,
            limit=min(limit, 500),
            offset=offset,
            fields=True
        )

        return await self.request(route)

    async def get_seasonal_anime(self, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            f'/anime/season/{year}/{season}',
            sort=sort,
            limit=min(limit, 500),
            offset=offset,
            fields=True
        )

        return await self.request(route)

    async def get_suggested_anime(self, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime/suggestions',
            limit=limit,
            offset=offset,
            fields=True
        )

        return await self.request(route)
