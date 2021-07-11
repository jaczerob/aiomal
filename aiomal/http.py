import asyncio

from typing import Any, ClassVar, Dict, Optional, Tuple
from urllib.parse import urljoin, urlencode

import aiohttp

from .errors import HTTPException, BadRequest, Unauthorized, Forbidden, NotFound
from .secrets import get_new_code_verifier


class Route:
    BASE: ClassVar[str] = 'https://api.myanimelist.net/'
    USER_AGENT: ClassVar[str] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.0) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/11.0 Safari/602.1.50'

    def __init__(self, method: str, path: str, version: int = 2, **parameters: Any) -> None:
        self.method = method
        self.path = path
        self.version = version
        self.parameters = parameters
        
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
    ANIME_FIELDS: ClassVar[str] = 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
    MANGA_FIELDS: ClassVar[str] = 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization{name}'
    USER_FIELDS: ClassVar[str] = 'id,name,picture,gender,birthday,location,joined_at,anime_statistics,time_zone,is_supporter'

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

    async def get_anime(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime',
            q=query,
            limit=min(limit, 100),
            offset=offset,
            fields=self.ANIME_FIELDS,
            access_token=access_token
        )

        return await self.request(route)

    async def get_anime_details(self, access_token: str, anime_id: int):
        route = Route(
            'GET',
            f'/anime/{anime_id}',
            fields=self.ANIME_FIELDS,
            access_token=access_token
        )

        return await self.request(route)

    async def get_anime_ranking(self, access_token: str, ranking_type: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime/ranking',
            ranking_type=ranking_type,
            limit=min(limit, 500),
            offset=offset,
            fields=self.ANIME_FIELDS,
            access_token=access_token
        )

        return await self.request(route)

    async def get_seasonal_anime(self, access_token: str, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            f'/anime/season/{year}/{season}',
            sort=sort,
            limit=min(limit, 500),
            offset=offset,
            fields=self.ANIME_FIELDS,
            access_token=access_token
        )

        return await self.request(route)

    async def get_suggested_anime(self, access_token: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/anime/suggestions',
            limit=min(limit, 100),
            offset=offset,
            fields=self.ANIME_FIELDS,
            access_token=access_token
        )

        return await self.request(route)

    async def update_anime_list_status(self, access_token: str, anime_id: int, **parameters):
        route = Route(
            'PATCH',
            f'/anime/{anime_id}/my_list_status',
            access_token=access_token,
            **parameters
        )

        return await self.request(route)

    async def delete_anime_list_item(self, access_token: str, anime_id: int):
        route = Route(
            'DELETE',
            f'/anime/{anime_id}/my_list_status',
            access_token=access_token
        )

        return await self.request(route)

    async def get_user_anime_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        parameters = {
            'sort': sort,
            'limit': min(limit, 1000),
            'offset': offset
        }

        if status:
            parameters['status'] = status

        route = Route(
            'GET',
            f'/users/{user_name}/animelist',
            access_token=access_token,
            **parameters
        )

        return await self.request(route)

    async def get_forum_boards(self, access_token: str):
        route = Route(
            'GET',
            '/forum/boards',
            access_token=access_token
        )

        return await self.request(route)

    async def get_forum_topic_detail(self, access_token: str, topic_id: int):
        route = Route(
            'GET',
            f'/forum/topic/{topic_id}',
            access_token=access_token
        )

        return await self.request(route)

    async def get_forum_topics(self, access_token: str):
        route = Route(
            'GET',
            '/forum/topics',
            access_token=access_token
        )

        return await self.request(route)

    async def get_manga_list(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/manga',
            access_token=access_token,
            query=query,
            limit=min(100, limit),
            fields=self.MANGA_FIELDS
        )

        return await self.request(route)

    async def get_manga_details(self, access_token: str, manga_id: int):
        route = Route(
            'GET',
            f'/manga/{manga_id}',
            access_token=access_token,
            fields=self.MANGA_FIELDS
        )

        return await self.request(route)

    async def get_manga_ranking(self, access_token: str, ranking_type: str = 'all', limit: int = 100, offset: int = 0):
        route = Route(
            'GET',
            '/manga/ranking',
            access_token=access_token,
            ranking_type=ranking_type,
            limit=min(limit, 500),
            offset=offset,
            fields=self.MANGA_FIELDS
        )

        return await self.request(route)

    async def update_manga_list_status(self, access_token: str, manga_id: int, **parameters):
        route = Route(
            'PATCH',
            f'/manga/{manga_id}/my_list_status',
            access_token=access_token,
            **parameters
        )

        return await self.request(route)

    async def delete_manga_list_item(self, access_token: str, manga_id: int):
        route = Route(
            'DELETE',
            f'/manga/{manga_id}/my_list_status',
            access_token=access_token
        )

        return await self.request(route)

    async def get_user_manga_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        parameters = {
            'sort': sort,
            'limit': min(limit, 1000),
            'offset': offset
        }

        if status:
            parameters['status'] = status

        route = Route(
            'GET',
            f'/users/{user_name}/mangalist',
            access_token=access_token,
            **parameters
        )

        return await self.request(route)

    async def get_user_information(self, access_token: str, user_name: str = '@me'):
        route = Route(
            'DELETE',
            f'/user/{user_name}',
            access_token=access_token,
            fields=self.USER_FIELDS
        )

        return await self.request(route)
