import asyncio

from typing import Any, ClassVar, Dict, Optional
from urllib.parse import urljoin, urlencode

import aiohttp

from .errors import HTTPException, BadRequest, Unauthorized, Forbidden, NotFound


class Route:
    BASE: ClassVar[str] = 'https://api.myanimelist.net/v2'
    FIELDS: ClassVar[str] = 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path
        
        self.parameters = parameters
        
        try:
            self.parameters.pop('fields')
            self.parameters['fields'] = self.FIELDS
        except KeyError:
            pass

        
    @property
    def url(self) -> str:
        return f'{urljoin(self.BASE, self.path)}?{urlencode(self.parameters)}'


class HTTPClient:
    def __init__(self) -> None:
        self.session: Optional[aiohttp.ClientSession] = None
        self.token: Optional[str] = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.0) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/11.0 Safari/602.1.50'

    async def request(self, route: Route):
        method = route.method
        url = route.url

        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
        }
        
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

    async def connect(self, token: str) -> None:
        self.session = aiohttp.ClientSession()
        self.token = token

        try:
            # Generic route for testing authorization
            data = await self.request(Route('GET', '/anime/suggestions', limit=4))
        except Unauthorized:
            raise
        except:
            raise

        return

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
