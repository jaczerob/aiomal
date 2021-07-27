from datetime import datetime
from typing import Any, Dict, List, Optional

from .generics import Object
from .subtypes import *


__all__ = [
    'User',
    'AnimeForList',
    'MangaForList',
    'AnimeDetails',
    'MangaDetails',
    'ForumCategory',
    'ForumTopicData',
    'ForumTopicsData'
]


class User(Object):
    """This class represents a MAL User
    
    Parameters
    -----------
    data: Dict[:class:`str`, Any]
        The JSON data returned from calling the API

    Attributes
    -----------
    id: :class:`int`
    
    
    """
    __slots__ = [
        'id', 
        'name', 
        'picture', 
        '_birthday', 
        'location', 
        '_joined_at',
        'anime_statistics', 
        'time_zone', 
        'is_supporter'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.picture: str = data.get('picture')
        self.gender: Optional[str] = data.get('gender')
        self._birthday: Optional[str] = data.get('birthday')
        self.location: Optional[str] = data.get('location')
        self._joined_at: str = data.get('joined_at')
        self.anime_statistics: Optional[AnimeStatistics] = AnimeStatistics(data.get('anime_statistics'))
        self.time_zone: Optional[str] = data.get('time_zone')
        self.is_supporter: Optional[bool] = data.get('is_supporter')

    @property
    def joined_at(self) -> datetime:
        return datetime.fromisoformat(self._joined_at)

    @property
    def birthday(self) -> Optional[datetime]:
        return date(self._birthday)


class MediaDetails:
    """__slots__ = [
        'pictures',
        'background',
        'related_anime',
        'related_manga',
        'recommendations',
    ]"""

    def __init__(self, data: Dict[str, Any], media_type: Media) -> None:
        self.pictures: List[Picture] = [Picture(picture) for picture in data.get('pictures')]
        self.background: str = data.get('background')
        self.related_anime: List[RelatedMediaEdge] = [RelatedMediaEdge(anime, AnimeForList) for anime in data.get('related_anime')]
        self.related_manga: List[RelatedMediaEdge] = [RelatedMediaEdge(manga, MangaForList) for manga in data.get('related_manga')]
        self.recommendations: List[MediaRecommendationAggregationEdgeBase] = [MediaRecommendationAggregationEdgeBase(item, media_type) for item in data.get('recommendations')]


class AnimeForList(Media):
    """__slots__ = [
        'num_episodes',
        'start_season',
        'broadcast',
        'source',
        'average_episode_duration',
        'rating',
        'studios'
    ]"""

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.num_episodes: int = data.get('num_episodes')
        self.start_season: StartSeason = StartSeason(data.get('start_season'))
        self.broadcast: Broadcast = Broadcast(data.get('broadcast'))
        self.source: str = data.get('source')
        self.average_episode_duration: int = data.get('average_episode_duration')
        self.rating: int = data.get('rating')
        self.studios: List[Studio] = [Studio(studio) for studio in data.get('studios', [])]


class AnimeDetails(AnimeForList, MediaDetails):
    """__slots__ = [
        'statistics'
    ]"""

    def __init__(self, data: Dict[str, Any]) -> None:
        MediaDetails.__init__(self, data, AnimeForList)
        AnimeForList.__init__(self, data)
        self.statistics: Statistics = Statistics(data.get('statistics'))


class MangaForList(Media):
    """__slots__ = [
        'num_volumes',
        'num_chapters',
        'authors',
    ]"""
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.num_volumes: int = data.get('num_volumes')
        self.num_chapters: int = data.get('num_chapters')
        self.authors: List[Author] = [Author(author) for author in data.get('authors', [])]


class MangaDetails(MangaForList, MediaDetails):
    """__slots__ = [
        'serialization'
    ]"""

    def __init__(self, data: Dict[str, Any]) -> None:
        MediaDetails.__init__(self, data, MangaForList)
        MangaForList.__init__(self, data)
        self.serialization: List[Serialization] = [Serialization(serialization) for serialization in data.get('serialization')]


class ForumCategory(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.title: str = data.get('title')
        self.boards: List[ForumBoard] = [ForumBoard(fb) for fb in data.get('boards')]


class ForumTopicData(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.title: str = data.get('title')
        self.posts: List[ForumTopicPost] = [ForumTopicPost(ftp) for ftp in data.get('posts')]
        self.poll: List[ForumTopicPoll] = [ForumTopicPoll(ftp) for ftp in data.get('poll', [])]


class ForumTopicsData(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.title: str = data.get('title')
        self.created_at: datetime = datetime.fromisoformat(data.get('created_at'))
        self.created_by: ForumTopicsCreatedBy = ForumTopicPostCreatedBy(data.get('created_by'))
        self.number_of_posts: int = data.get('number_of_posts')
        self.last_post_created_at: datetime = datetime.fromisoformat(data.get('last_post_created_at'))
        self.last_post_created_by: ForumTopicsCreatedBy = ForumTopicPostCreatedBy(data.get('last_post_created_by'))
        self.is_locked: bool = data.get('is_locked')
