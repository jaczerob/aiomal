from aiomal.objects.subtypes import MyListStatus
from typing import List, Optional, Tuple

from .errors import NotFound
from .http import HTTPClient
from .objects.maintypes import *


class ClientUser:
    """A class used to interact with the MAL API with a user's access token
    
    Do not make this directly, use the :class:`Client` method :method:`make_user`
    """
    def __init__(self, access_token: str, refresh_token: str, http: HTTPClient) -> None:
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._http = http

    async def get_anime(self, query: str, limit: int = 100, offset: int = 0) -> List[AnimeForList]:
        """Returns anime matching the query

        Parameters
        -----------
        query: :class:`str`
            What to search in the MAL database

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 100. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start.

        Returns
        --------
        List[:class:`AnimeForList`]
            A list of anime that matched the given query
        """
        data = await self._http.get_anime(self._access_token, query, limit, offset)
        anime = [AnimeForList(a['node']) for a in data['data']]
        return anime

    async def get_anime_details(self, anime_id: int) -> AnimeDetails:
        """Returns the details of the anime with the given ID
        
        Parameters
        -----------
        anime_id: :class:`id`
            The anime's ID in the MAL database

        Returns
        --------
        :class:`AnimeDetails`
            An object containing the details of the anime
        """
        data = await self._http.get_anime_details(self._access_token, anime_id)
        anime = AnimeDetails(data)
        return anime

    async def get_anime_ranking(self, ranking_type: str, limit: int = 100, offset: int = 0) -> List[AnimeForList]:
        """Gets the ranking from [1 + offset, offset + limit]
        
        Parameters
        -----------
        ranking_type: :class:`str`
            The criteria ranking will be based on.
            Options include: all, airing, upcoming, tv, ova, movie, special, bypopularity, favorite

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start.

        Returns
        --------
        List[:class:`AnimeForList`]
            The ranking by the given ranking type
        """
        data = await self._http.get_anime_ranking(self._access_token, ranking_type, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime

    async def get_seasonal_anime(self, year: int, season: str, sort: str = 'anime_score', limit: int = 100, offset: int = 0) -> List[AnimeForList]:
        data = await self._http.get_seasonal_anime(self._access_token, year, season, sort, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime

    async def get_suggested_anime(self, limit: int = 100, offset: int = 0) -> List[AnimeForList]:
        data = await self._http.get_suggested_anime(self._access_token, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime
    
    async def update_anime_list_status(self, anime_id: int, **parameters) -> MyListStatus:
        data = await self._http.update_anime_list_status(self._access_token, anime_id, **parameters)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_anime_list_item(self, anime_id: int) -> bool:
        try:
            await self._http.delete_anime_list_item(self._access_token, anime_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_anime_list(self, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0) -> Tuple[AnimeForList, MyListStatus]:
        data = await self._http.get_user_anime_list(self._access_token, user_name, status, sort, limit, offset)
        
        # TODO: make a cleaner type for this
        user_anime_list = [(AnimeForList(anime['node']), MyListStatus(anime['list_status'])) for anime in data['data']]
        return user_anime_list

    async def get_forum_boards(self) -> List[ForumCategory]:
        data = await self._http.get_forum_boards(self._access_token)
        forum_boards = [ForumCategory(fc) for fc in data['categories']]
        return forum_boards

    async def get_forum_topic_detail(self, topic_id: int) -> List[ForumTopicData]:
        data = await self._http.get_forum_topic_detail(self._access_token, topic_id)
        forum_topics_detail = [ForumTopicData(ftd) for ftd in data['data']]
        return forum_topics_detail

    async def get_forum_topics(self) -> List[ForumTopicsData]:
        data = await self._http.get_forum_topics(self._access_token)
        forum_topics = [ForumTopicsData(ftd) for ftd in data['data']]
        return forum_topics

    async def get_manga_list(self, query: str, limit: int = 100, offset: int = 0) -> List[MangaForList]:
        data = await self._http.get_manga_list(self._access_token, query, limit, offset)
        manga = [MangaForList(m['node']) for m in data['data']]
        return manga

    async def get_manga_details(self, manga_id: int) -> MangaDetails:
        data = await self._http.get_manga_details(self._access_token, manga_id)
        manga = MangaDetails(data)
        return manga

    async def get_manga_ranking(self, ranking_type: str = 'all', limit: int = 100, offset: int = 0) -> List[MangaForList]:
        data = await self._http.get_manga_ranking(self._access_token, ranking_type, limit, offset)
        manga = [MangaForList(m) for m in data['data']]
        return manga

    async def update_manga_list_status(self, manga_id: int, **parameters) -> MyListStatus:
        data = await self._http.update_manga_list_status(self._access_token, manga_id, **parameters)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_manga_list_item(self, manga_id: int) -> bool:
        try:
            await self._http.delete_manga_list_item(self._access_token, manga_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_manga_list(self, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0) -> List[MangaForList]:
        data = await self._http.get_user_manga_list(self._access_token, user_name, status, sort, limit, offset)
        manga = [MangaForList(m['node']) for m in data['data']]
        return manga

    async def get_user_information(self, user_name: str = '@me') -> User:
        data = await self._http.get_user_information(self._access_token, user_name)
        user = User(data)
        return user


class Client:
    """A client class that deals with authentication and creating :class:`ClientUser`s to interact with
    the MAL API

    Parameters
    -----------
    client_id: :class:`str`
        The client ID of the developer application obtained from the MAL API config
    
    client_secret: :class:`str`
        The client secret of the developer application obtained from the MAL API config
    """
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._http = HTTPClient(client_id, client_secret)

    def generate_auth_url(self) -> str:
        """Returns an auth URL for end users to obtain their auth code
        
        Returns
        --------
        :class:`str`
            The generated auth URL
        """
        return self._http.generate_auth_url()

    async def generate_access_token(self, auth_code: str, code_verifier: str) -> Tuple[str, str]:
        """Returns an access token and refresh token for the user to gain access to the API

        Parameters
        -----------
        auth_code: :class:`str`
            The user's auth code obtained from their given auth URL

        code_verifier: :class:`str`
            The user's unique code challenge
        
        Returns
        --------
        Tuple[:class:`str`, :class:`str`]
            A tuple containing the access token and refresh token for the user
        """
        return await self._http.generate_access_token(auth_code, code_verifier)

    def make_user(self, access_token: str, refresh_token: str) -> ClientUser:
        """Returns a :class:`ClientUser` that can interact with the MAL API

        Parameters
        -----------
        access_token: :class:`str`
            The user's access token obtained from their given auth URL

        refresh_token: :class:`str`
            The user's refresh token obtained from their given auth URL
        
        Returns
        --------
        :class:`ClientUser`
            An object used to interact with the MAL API
        """
        return ClientUser(access_token, refresh_token, self._http)
