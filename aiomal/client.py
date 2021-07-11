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
