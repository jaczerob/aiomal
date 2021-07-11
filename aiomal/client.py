from .http import HTTPClient


class Client:
    def __init__(self, token: str) -> None:
        self.token = token
        self.http = HTTPClient()

    async def connect(self) -> None:
        await self.http.connect(self.token)

    async def get_anime(self, query: str, limit: int = 100, offset: int = 0):
        return await self.http.get_anime(query, limit, offset)

    async def get_anime_details(self, anime_id: int):
        return await self.http.get_anime_details(anime_id)

    async def get_anime_ranking(self, ranking_type: str, limit: int = 100, offset: int = 0):
        return await self.http.get_anime_ranking(ranking_type, limit, offset)

    async def get_seasonal_anime(self, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0):
        return await self.http.get_seasonal_anime(year, season, sort, limit, offset)

    async def get_suggested_anime(self, limit: int = 100, offset: int = 0):
        return await self.http.get_suggested_anime(limit, offset)
