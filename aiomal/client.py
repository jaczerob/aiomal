from typing import List, Optional, Tuple

from .errors import NotFound
from .http import HTTPClient
from .objects.maintypes import *
from .objects.subtypes import MyListStatus


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
        """Returns all the anime released in a season and year
        
        Parameters
        -----------
        year: :class:`int`
            The year to query

        season: :class:`str`
            The season to query 
            Options: winter, spring, summer, fall
        
        sort: :class:`str`
            The criteria for how the ranking will be based
            Options: anime_score, anime_num_list_users

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start

        Returns
        --------
        List[:class:`AnimeForList`]
            A list of the anime in the given season and year
        """
        data = await self._http.get_seasonal_anime(self._access_token, year, season, sort, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime

    async def get_suggested_anime(self, limit: int = 100, offset: int = 0) -> List[AnimeForList]:
        """Returns suggested anime for the user

        If the user is new comer, this method returns an empty list
        
        Parameters
        -----------
        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start
        
        Returns
        --------
        List[:class:`AnimeForList`]
            A list of suggested anime for the user
        """
        data = await self._http.get_suggested_anime(self._access_token, limit, offset)
        anime = [AnimeForList(a) for a in data['data']]
        return anime
    
    async def update_anime_list_status(self, anime_id: int, **kwargs) -> MyListStatus:
        """Add specified anime to my anime list

        If specified anime already exists, update its status
        
        Parameters
        -----------
        anime_id: :class:`int`
            The ID of the anime to update

        kwargs:
            status: :class:`str`
                watching, completed, on_hold, dropped, plan_to_watch

            is_rewatching: :class:`bool`
            
            score: :class:`int`
                0-10

            num_watched_episodes: :class:`int`

            priority: :class:`int`
                0-2

            num_times_rewatched: :class:`int`
            
            rewatch_value: :class:`int`
                0-5

            tags: :class:`str`
            
            comments: :class:`str`

        Returns
        --------
        :class:`MyListStatus`
            An object for the status of the given anime
        """
        data = await self._http.update_anime_list_status(self._access_token, anime_id, **kwargs)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_anime_list_item(self, anime_id: int) -> bool:
        """Deletes an anime from the user's anime list
        
        Parameters
        -----------
        anime_id: :class:`int`
            The ID of the anime to delete
        
        Returns
        --------
        :class:`bool`
            True if the anime was deleted successfully, False if the anime was not found
        """
        try:
            await self._http.delete_anime_list_item(self._access_token, anime_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_anime_list(self, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0) -> List[Tuple[AnimeForList, MyListStatus]]:
        """Returns the given user's anime list
        
        Parameters
        -----------
        user_name: :class:`str`
            The user name of the user to query, default @me

        status: :class:`str`
            Filter returned anime list by the given status
            Options: watching, completed, on_hold, dropped, plan_to_watch

        sort: :class:`str`
            Sort the returned anime list by the given criteria
            Options: list_score, list_updated_at, anime_title, anime_start_date, anime_id

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start
        
        Returns
        --------
        List[Tuple[:class:`AnimeForList`, :class:`MyListStatus`]]
            A list of each anime and their status
        """
        data = await self._http.get_user_anime_list(self._access_token, user_name, status, sort, limit, offset)
        
        # TODO: make a cleaner type for this
        user_anime_list = [(AnimeForList(anime['node']), MyListStatus(anime['list_status'])) for anime in data['data']]
        return user_anime_list

    async def get_forum_boards(self) -> List[ForumCategory]:
        """Returns the main forum boards (MyAnimeList, Anime & Manga, General)
        
        Returns
        --------
        List[:class:`ForumCategory`]
            A list of the forum boards
        """
        data = await self._http.get_forum_boards(self._access_token)
        forum_boards = [ForumCategory(fc) for fc in data['categories']]
        return forum_boards

    async def get_forum_topic_detail(self, topic_id: int) -> List[ForumTopicData]:
        """Returns the topic data of the topic ID
        
        Parameters
        -----------
        topic_id: :class:`int`
            The ID of the topic
        
        Returns
        --------
        List[:class:`ForumTopicData`]
            The forum topic data containing every post and poll in a forum topic
        """
        data = await self._http.get_forum_topic_detail(self._access_token, topic_id)
        forum_topics_detail = [ForumTopicData(ftd) for ftd in data['data']]
        return forum_topics_detail

    async def get_forum_topics(self, board_id: Optional[int] = None, subboard_id: Optional[int] = None, limit: int = 100, offset: int = 0, sort: str = 'recent', q: Optional[str] = None, topic_user_name: Optional[str] = None, user_name: Optional[str] = None) -> List[ForumTopicsData]:
        """Return forum topics under given queries
        
        Parameters
        -----------
        board_id: Optional[:class:`int`]
            The forum board ID

        subboard_id: Optional[:class:`int`]
            The subboard ID

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 100. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start

        sort: :class:`str`
            How to sort the forum topics
            Options: recent

        q: :class:`str`
            Keywords to search for forum topics

        topic_user_name: :class:`str`
            The user name of the topic creator

        user_name: :class:`str`
            A user name to search for forum topics created by
        
        Returns
        --------
        List[`ForumTopicsData`]
            A list of all forum topics matching the given query
        """
        data = await self._http.get_forum_topics(self._access_token, board_id, subboard_id, limit, offset, sort, q, topic_user_name, user_name)
        forum_topics = [ForumTopicsData(ftd) for ftd in data['data']]
        return forum_topics

    async def get_manga(self, query: str, limit: int = 100, offset: int = 0) -> List[MangaForList]:
        """Returns manga matching the query

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
        List[:class:`MangaForList`]
            A list of manga that matched the given query
        """
        data = await self._http.get_manga(self._access_token, query, limit, offset)
        manga = [MangaForList(m['node']) for m in data['data']]
        return manga

    async def get_manga_details(self, manga_id: int) -> MangaDetails:
        """Returns the details of the manga with the given ID
        
        Parameters
        -----------
        manga_id: :class:`id`
            The manga's ID in the MAL database

        Returns
        --------
        :class:`MangaDetails`
            An object containing the details of the manga
        """
        data = await self._http.get_manga_details(self._access_token, manga_id)
        manga = MangaDetails(data)
        return manga

    async def get_manga_ranking(self, ranking_type: str = 'all', limit: int = 100, offset: int = 0) -> List[MangaForList]:
        """Gets the ranking from [1 + offset, offset + limit]
        
        Parameters
        -----------
        ranking_type: :class:`str`
            The criteria ranking will be based on.
            Options include: all, manga, oneshots, doujin, lightnovels, novels, manhwa, manhua, bypopularity, favorite

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start.

        Returns
        --------
        List[:class:`MangaForList`]
            The ranking by the given ranking type
        """
        data = await self._http.get_manga_ranking(self._access_token, ranking_type, limit, offset)
        manga = [MangaForList(m) for m in data['data']]
        return manga

    async def update_manga_list_status(self, manga_id: int, **kwargs) -> MyListStatus:
        """Add specified manga to my manga list

        If specified manga already exists, update its status
        
        Parameters
        -----------
        manga_id: :class:`int`
            The ID of the manga to update

        kwargs:
            status: :class:`str`
                reading, completed, on_hold, dropped, plan_to_read

            is_rereading: :class:`bool`
            
            score: :class:`int`
                0-10

            num_volumes_read: :class:`int`

            num_chapters_read: :class:`int`

            priority: :class:`int`
                0-2

            num_times_reread: :class:`int`
            
            reread_value: :class:`int`
                0-5

            tags: :class:`str`
            
            comments: :class:`str`

        Returns
        --------
        :class:`MyListStatus`
            An object for the status of the given manga
        """
        data = await self._http.update_manga_list_status(self._access_token, manga_id, **kwargs)
        my_list_status = MyListStatus(data)
        return my_list_status

    async def delete_manga_list_item(self, manga_id: int) -> bool:
        """Deletes an manga from the user's manga list
        
        Parameters
        -----------
        manga_id: :class:`int`
            The ID of the manga to delete
        
        Returns
        --------
        :class:`bool`
            True if the manga was deleted successfully, False if the manga was not found
        """
        try:
            await self._http.delete_manga_list_item(self._access_token, manga_id)
        except NotFound:
            return False
        else:
            return True

    async def get_user_manga_list(self, user_name: str = '@me', status: Optional[str] = None, sort: str = 'list_score', limit: int = 100, offset: int = 0) -> Tuple[MangaForList, MyListStatus]:
        """Returns the given user's manga list
        
        Parameters
        -----------
        user_name: :class:`str`
            The user name of the user to query, default @me

        status: :class:`str`
            Filter returned manga list by the given status
            Options: reading, completed, on_hold, dropped, plan_to_read

        sort: :class:`str`
            Sort the returned manga list by the given criteria
            Options: list_score, list_updated_at, manga_title, manga_start_date, manga_id

        limit: :class:`int`
            The max amount of results to return. Cannot exceed 500. Defaults to 100.

        offset: :class:`int`
            The offset from 1 for where the list will start
        
        Returnshmm
        --------
        List[Tuple[:class:`MangaForList`, :class:`MyListStatus`]]
            A list of each anime and their status
        """
        data = await self._http.get_user_manga_list(self._access_token, user_name, status, sort, limit, offset)

        # TODO: make a cleaner type for this
        user_manga_list = [MangaForList(manga['node'], MyListStatus(manga['list_status'])) for manga in data['data']]
        return user_manga_list

    async def get_user_information(self, user_name: str = '@me') -> User:
        """Gets the user's information
        
        Parameters
        -----------
        user_name: :class:`str`
            The user to search, defaults to @me
        
        Returns
        --------
        :class:`User`
            The user's information
        """
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
