from os import access
from typing import Optional
from .http import HTTPClient


class Client:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.http = HTTPClient(client_id, client_secret)

    def generate_auth_url(self):
        return self.http.generate_auth_url()

    async def generate_access_token(self, auth_code: str, code_verifier: str):
        return await self.http.generate_access_token(auth_code, code_verifier)

    async def get_anime(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        return await self.http.get_anime(access_token, query, limit, offset)

    async def get_anime_details(self, access_token: str, anime_id: int):
        return await self.http.get_anime_details(access_token, anime_id)

    async def get_anime_ranking(self, access_token: str, ranking_type: str, limit: int = 100, offset: int = 0):
        return await self.http.get_anime_ranking(access_token, ranking_type, limit, offset)

    async def get_seasonal_anime(self, access_token: str, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0):
        return await self.http.get_seasonal_anime(access_token, year, season, sort, limit, offset)

    async def get_suggested_anime(self, access_token: str, limit: int = 100, offset: int = 0):
        return await self.http.get_suggested_anime(access_token, limit, offset)
    
    async def update_anime_list_status(self, access_token: str, anime_id: int, **parameters):
        return await self.http.update_anime_list_status(access_token, anime_id, **parameters)

    async def delete_anime_list_item(self, access_token: str, anime_id: int):
        return await self.http.delete_anime_list_item(access_token, anime_id)

    async def get_user_anime_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        return await self.http.get_user_anime_list(access_token, user_name, status, sort, limit, offset)

    async def get_forum_boards(self, access_token: str):
        return await self.http.get_forum_boards(access_token)

    async def get_forum_topic_detail(self, access_token: str, topic_id: int):
        return await self.http.get_forum_topic_detail(access_token, topic_id)

    async def get_forum_topics(self, access_token: str):
        return await self.http.get_forum_topics(access_token)

    async def get_manga_list(self, access_token: str, query: str, limit: int = 100, offset: int = 0):
        return await self.http.get_manga_list(access_token, query, limit, offset)

    async def get_manga_details(self, access_token: str, manga_id: int):
        return await self.http.get_manga_details(access_token, manga_id)

    async def get_manga_ranking(self, access_token: str, ranking_type: str = 'all', limit: int = 100, offset: int = 0):
        return await self.http.get_manga_ranking(access_token, ranking_type, limit, offset)

    async def update_manga_list_status(self, access_token: str, manga_id: int, **parameters):
        return await self.http.update_manga_list_status(access_token, manga_id, **parameters)

    async def delete_manga_list_item(self, access_token: str, manga_id: int):
        return await self.http.delete_manga_list_item(access_token, manga_id)

    async def get_user_manga_list(self, access_token: str, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0):
        return await self.http.get_user_manga_list(access_token, user_name, status, sort, limit, offset)

    async def get_user_information(self, access_token: str, user_name: str = '@me'):
        return await self.http.get_user_information(access_token, user_name)