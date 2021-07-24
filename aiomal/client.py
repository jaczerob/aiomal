from aiomal.objects.subtypes import MyListStatus
from typing import Optional

from .errors import NotFound
from .http import HTTPClient
from .objects.maintypes import *


class Client:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.http = HTTPClient(client_id, client_secret)

    def generate_auth_url(self):
        return self.http.generate_auth_url()

    async def generate_access_token(self, auth_code: str, code_verifier: str):
        return await self.http.generate_access_token(auth_code, code_verifier)

    async def get_anime(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        data = await self.http.get_anime(access_token, query, limit, offset)
        anime = [AnimeForList(a['node']) for a in data['data']]
        return anime

    async def get_anime_details(self, access_token: str, anime_id: int):
        data = await self.http.get_anime_details(access_token, anime_id)
        anime = AnimeDetails(data)
        return anime

    async def get_anime_ranking(self, access_token: str, ranking_type: str, limit: int = 100, offset: int = 0):
        data = await self.http.get_anime_ranking(access_token, ranking_type, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime

    async def get_seasonal_anime(self, access_token: str, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0):
        data = await self.http.get_seasonal_anime(access_token, year, season, sort, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime

    async def get_suggested_anime(self, access_token: str, limit: int = 100, offset: int = 0):
        data = await self.http.get_suggested_anime(access_token, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime
    
    async def update_anime_list_status(self, access_token: str, anime_id: int, **parameters):
        data = await self.http.update_anime_list_status(access_token, anime_id, **parameters)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_anime_list_item(self, access_token: str, anime_id: int):
        try:
            await self.http.delete_anime_list_item(access_token, anime_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_anime_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        data = await self.http.get_user_anime_list(access_token, user_name, status, sort, limit, offset)
        
        # make a type for this
        user_anime_list = [(AnimeForList(anime['node']), MyListStatus(anime['list_status'])) for anime in data['data']]
        return user_anime_list

    async def get_forum_boards(self, access_token: str):
        data = await self.http.get_forum_boards(access_token)
        forum_boards = [ForumCategory(fc) for fc in data['categories']]
        return forum_boards

    async def get_forum_topic_detail(self, access_token: str, topic_id: int):
        data = await self.http.get_forum_topic_detail(access_token, topic_id)
        forum_topics_detail = [ForumTopicData(ftd) for ftd in data['data']]
        return forum_topics_detail

    async def get_forum_topics(self, access_token: str):
        data = await self.http.get_forum_topics(access_token)
        forum_topics = [ForumTopicsData(ftd) for ftd in data['data']]
        return forum_topics

    async def get_manga_list(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        data = await self.http.get_manga_list(access_token, query, limit, offset)
        manga = [MangaForList(m['node']) for m in data['data']]
        return manga

    async def get_manga_details(self, access_token: str, manga_id: int):
        data = await self.http.get_manga_details(access_token, manga_id)
        manga = MangaDetails(data)
        return manga

    async def get_manga_ranking(self, access_token: str, ranking_type: str = 'all', limit: int = 100, offset: int = 0):
        data = await self.http.get_manga_ranking(access_token, ranking_type, limit, offset)
        manga = [MangaForList(m) for m in data['data']]
        return manga

    async def update_manga_list_status(self, access_token: str, manga_id: int, **parameters):
        data = await self.http.update_manga_list_status(access_token, manga_id, **parameters)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_manga_list_item(self, access_token: str, manga_id: int):
        try:
            await self.http.delete_manga_list_item(access_token, manga_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_manga_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        data = await self.http.get_user_manga_list(access_token, user_name, status, sort, limit, offset)
        manga = [MangaForList(m['node']) for m in data['data']]
        return manga

    async def get_user_information(self, access_token: str, user_name: str = '@me'):
        data = await self.http.get_user_information(access_token, user_name)
        user = User(data)
        return user