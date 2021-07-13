from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Generic


class AlternativeTitles:
    __slots__ = [
        'synonyms',
        'en',
        'jp'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.synonyms: List[str] = data.get('synonyms')
        self.en: str = data.get('en')
        self.jp: str = data.get('jp')


class AnimeStatistics:
    __slots__ = [
        'num_items_watching',
        'num_items_completed',
        'num_items_on_hold',
        'num_items_dropped',
        'num_items_plan_to_watch',
        'num_items',
        'num_days_watched',
        'num_days_watching',
        'num_days_completed',
        'num_days_on_hold',
        'num_days_dropped',
        'num_days',
        'num_episodes',
        'num_times_rewatched',
        'mean_score'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.num_items_watching: int = data.get('num_items_watching')
        self.num_items_completed: int = data.get('num_items_completed')
        self.num_items_on_hold: int = data.get('num_items_on_hold')
        self.num_items_dropped: int = data.get('num_items_dropped')
        self.num_items_plan_to_watch: int = data.get('num_items_plan_to_watch')
        self.num_items: int = data.get('num_items')
        self.num_days_watched: float = data.get('num_days_watched')
        self.num_days_watching: float = data.get('num_days_watching')
        self.num_days_completed: float = data.get('num_days_completed')
        self.num_days_on_hold: float = data.get('num_days_on_hold')
        self.num_days_dropped: float = data.get('num_days_dropped')
        self.num_days: float = data.get('num_days')
        self.num_episodes: int = data.get('num_episodes')
        self.num_times_rewatched: int = data.get('num_times_rewatched')
        self.mean_score: int = data.get('mean_score')


class Picture:
    __slots__ = [
        'large',
        'medium'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.large = data.get('large')
        self.medium = data.get('medium')


class Genre:
    __slots__ = [
        'id',
        'name'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: int = data.get('id')
        self.name: str = data.get('name')


class MyListStatus:
    __slots__ = [
        'status',
        'score',
        'num_watched_episodes',
        'is_rewatching',
        'start_date',
        'finish_date',
        'priority',
        'num_times_rewatched',
        'rewatch_value',
        'tags',
        'comments',
        'updated_at'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.status: str = data.get('status')
        self.score: int = data.get('score')
        self.num_watched_episodes: int = data.get('num_watched_episodes')
        self.is_rewatching: bool = data.get('is_rewatching')
        self.start_date: datetime = datetime.strptime('%Y-%m-%d', data.get('start_date'))
        self.finish_date: datetime = datetime.strptime('%Y-%m-%d', data.get('finish_date'))
        self.priority: int = data.get('priority')
        self.num_times_rewatched: int = data.get('num_times_rewatched')
        self.rewatch_value: int = data.get('rewatch_value')
        self.tags: List[str] = data.get('tags')
        self.comments: str = data.get('comments')
        self.updated_at: datetime = datetime.fromisoformat(data.get('updated_at'))


class StartSeason:
    __slots__ = [
        'year',
        'season'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.year: int = data.get('year')
        self.season: str = data.get('season')


class Broadcast:
    __slots__ = [
        'day_of_the_week',
        'start_time'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.day_of_the_week: str = data.get('day_of_the_week')
        self.start_time: str = data.get('start_time')


class Studio:
    __slots__ = [
        'id',
        'name'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: int = data.get('id')
        self.name: str = data.get('name')


T = TypeVar('T')


class RelatedEdge(Generic[T]):
    __slots__ = [
        'node',
        'relation_type',
        'relation_type_formatted'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.node: T = data.get('node')
        self.relation_type: str = data.get('relation_type')
        self.relation_type_formatted: str = data.get('relation_type_formatted')


class RecommendationAggregationEdgeBase(Generic[T]):
    __slots__ = [
        'node',
        'num_recommendations'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.node: T = data.get('node')
        self.num_recommendations = data.get('num_recommendations')


class Status:
    __slots__ = [
        'watching',
        'completed',
        'on_hold',
        'dropped',
        'plan_to_watch'
    ]
    
    def __init__(self, data: Dict[str, Any]) -> None:
        self.watching: int = data.get('watching')
        self.completed: int = data.get('completed')
        self.on_hold: int = data.get('on_hold')
        self.dropped: int = data.get('dropped')
        self.plan_to_watch: int = data.get('plan_to_watch')


class Statistics:
    __slots__ = [
        'num_list_users',
        'status'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.num_list_users: int = data.get('num_list_users')
        self.status: Status = Status(data.get('status'))


class Author:
    __slots__ = [
        'id',
        'first_name',
        'last_name',
        'role'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: int = data.get('node').get('id')
        self.first_name: str = data.get('node').get('first_name')
        self.last_name: str = data.get('node').get('last_name')
        self.role: str = data.get('role')


class Serialization:
    __slots__ = [
        'id',
        'name',
        'role'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id = data.get('node').get('id')
        self.name = data.get('node').get('name')
        self.role = data.get('role')


class User:
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
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.picture: str = data.get('picture')
        self._birthday: str = data.get('birthday')
        self.location: str = data.get('location')
        self._joined_at: str = data.get('joined_at')
        self.anime_statistics: AnimeStatistics = AnimeStatistics(data.get('anime_statistics'))
        self.time_zone: str = data.get('time_zone')
        self.is_supporter: bool = data.get('is_supporter')

    @property
    def joined_at(self) -> datetime:
        return datetime.fromisoformat(self._joined_at)

    @property
    def birthday(self) -> datetime:
        return datetime.strptime('%Y-%m-%d', self._birthday)


class _Media(Generic[T]):
    __slots__ = [
        'id',
        'title',
        'main_picture',
        'alternative_titles',
        'start_date',
        'end_date',
        'synopsis',
        'mean',
        'rank',
        'popularity',
        'num_list_users',
        'nsfw',
        'genres',
        '_created_at',
        '_updated_at',
        'media_type',
        'status',
        'my_list_status',
        'pictures',
        'background',
        'related_anime',
        'related_manga',
        'recommendations'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: int = data.get('id')
        self.title: str = data.get('title')
        self.main_picture: Picture = Picture(data.get('main_picture'))
        self.alternative_titles: AlternativeTitles = AlternativeTitles(data.get('alternative_titles'))
        self.start_date: str = data.get('start_date')
        self.end_date: str = data.get('end_date')
        self.synopsis: str = data.get('synopsis')
        self.mean: Optional[float] = data.get('mean', None)
        self.rank: Optional[int] = data.get('rank', None)
        self.popularity: int = data.get('popularity')
        self.num_list_users: int = data.get('num_list_users')
        self.nsfw: str = data.get('nsfw')
        self.genres: List[Genre] = [Genre(genre) for genre in data.get('genres')]
        self._created_at: str = data.get('created_at')
        self._updated_at: str = data.get('updated_at')
        self.media_type: str = data.get('media_type')
        self.status: str = data.get('status')
        self.my_list_status: Optional[MyListStatus] = data.get('my_list_status', None)
        self.pictures: List[Picture] = [Picture(picture) for picture in data.get('pictures')]
        self.background: str = data.get('background')
        self.related_anime: List[RelatedEdge[T]] = [RelatedEdge[T](anime) for anime in data.get('related_anime')]
        self.related_manga: List[RelatedEdge[T]] = [RelatedEdge[T](manga) for manga in data.get('related_manga')]
        self.recommendations: List[RecommendationAggregationEdgeBase[T]] = [RecommendationAggregationEdgeBase[T](anime) for anime in data.get('recommendations')]

    @property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._created_at)

    @property
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._updated_at)


class _Anime(_Media):
    __slots__ = [
        'num_episodes',
        'start_season',
        'broadcast',
        'source',
        'average_episode_duration',
        'rating',
        'studios',
        'statistics'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.num_episodes: int = data.get('num_episodes')
        self.start_season: StartSeason = StartSeason(data.get('start_season'))
        self.broadcast: Broadcast = Broadcast(data.get('broadcast'))
        self.source: str = data.get('source')
        self.average_episode_duration: int = data.get('average_episode_duration')
        self.rating: int = data.get('rating')
        self.studios: List[Studio] = [Studio(studio) for studio in data.get('studios')]
        self.statistics: Statistics = Statistics(data.get('statistics'))


class _Manga(_Media):
    __slots__ = [
        'num_volumes',
        'num_chapters',
        'authors',
        'serialization'
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.num_volumes: int = data.get('num_volumes')
        self.num_chapters: int = data.get('num_chapters')
        self.authors: List[Author] = [Author(author) for author in data.get('authors')]
        self.serialization: List[Serialization] = [Serialization(serialization) for serialization in data.get('serialization')]


Anime = _Anime[_Anime]
Manga = _Manga[_Manga]
