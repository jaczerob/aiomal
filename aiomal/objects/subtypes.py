from datetime import datetime
from typing import Any, Dict, List, Optional

from .generics import Object, Nullable


__all__ = [
    'date',
    'AlternativeTitles',
    'AnimeStatistics',
    'Author',
    'Broadcast',
    'ForumBoard',
    'ForumTopicsCreatedBy',
    'ForumSubboard',
    'ForumTopicPost',
    'ForumTopicPostCreatedBy',
    'ForumTopicPoll',
    'ForumTopicPollOption',
    'Genre',
    'Media',
    'MediaRecommendationAggregationEdgeBase',
    'MyListStatus',
    'Picture',
    'RelatedMediaEdge',
    'Serialization',
    'StartSeason',
    'Statistics',
    'Status',
    'Studio',
]


def date(string: Optional[str]) -> Optional[datetime]:
    if string is None:
        return None

    return datetime.strptime('%Y-%m-%d', string)


class AlternativeTitles(Nullable):
    __slots__ = ['synonyms', 'en', 'jp']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.synonyms: Optional[List[str]] = data.get('synonyms', None)
        self.en: Optional[str] = data.get('en', None)
        self.jp: Optional[str] = data.get('jp', None)


class AnimeStatistics(Nullable):
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
        super().__init__(data)
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


class Author(Object):
    __slots__ = ['id', 'first_name', 'last_name', 'role']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('node').get('id')
        self.first_name: str = data.get('node').get('first_name')
        self.last_name: str = data.get('node').get('last_name')
        self.role: str = data.get('role')


class Broadcast(Nullable):
    __slots__ = ['day_of_the_week', 'start_time']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.day_of_the_week: Optional[str] = data.get('day_of_the_week', None)
        self.start_time: Optional[str] = data.get('start_time', None)


class ForumBoard(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.title: str = data.get('title')
        self.description: str = data.get('description')
        self.subboards: List[ForumSubboard] = [ForumSubboard(fs) for fs in data.get('subboards')]


class ForumSubboard(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.title: str = data.get('title')


class ForumTopicsCreatedBy(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')


class ForumTopicPost(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.number: int = data.get('number')
        self.created_at: datetime = datetime.fromisoformat(data.get('created_at'))
        self.created_by: ForumTopicPostCreatedBy = ForumTopicPostCreatedBy(data.get('created_by'))
        self.body: str = data.get('body')
        self.signature: str = data.get('signature')


class ForumTopicPostCreatedBy(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.forum_avator: str = data.get('forum_avator')


class ForumTopicPoll(Nullable):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.question: str = data.get('question')
        self.close: bool = data.get('close')
        self.options: ForumTopicPollOption = ForumTopicPollOption(data.get('options'))


class ForumTopicPollOption(Object):
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.text: str = data.get('text')
        self.votes: int = data.get('votes')


class Genre(Object):
    __slots__ = ['id', 'name']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')


class Media(Object):
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
    ]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.title: str = data.get('title')
        self.main_picture: Picture = Picture(data.get('main_picture'))
        self.alternative_titles: AlternativeTitles = AlternativeTitles(data.get('alternative_titles') or {})
        self.start_date: str = data.get('start_date')
        self.end_date: str = data.get('end_date')
        self.synopsis: str = data.get('synopsis')
        self.mean: Optional[float] = data.get('mean', None)
        self.rank: Optional[int] = data.get('rank', None)
        self.popularity: int = data.get('popularity')
        self.num_list_users: int = data.get('num_list_users')
        self.nsfw: str = data.get('nsfw')
        self.genres: List[Genre] = [Genre(genre) for genre in data.get('genres', [])]
        self._created_at: str = data.get('created_at')
        self._updated_at: str = data.get('updated_at')
        self.media_type: str = data.get('media_type')
        self.status: str = data.get('status')
        self.my_list_status: Optional[MyListStatus] = data.get('my_list_status', None)

    @property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._created_at)

    @property
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._updated_at)

    def __repr__(self) -> str:
        return f'<{type(self).__name__} name={self.title}>'

    def __str__(self) -> str:
        return self.title


class MediaRecommendationAggregationEdgeBase(Object):
    __slots__ = ['node', 'num_recommendations']

    def __init__(self, data: Dict[str, Any], media_type) -> None:
        self.media: media_type = media_type(data.get('node'))
        self.num_recommendations = data.get('num_recommendations')


class MyListStatus(Nullable):
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
        super().__init__(data)
        self.status: Optional[str] = data.get('status', None)
        self.score: int = data.get('score')
        self.num_watched_episodes: int = data.get('num_watched_episodes')
        self.is_rewatching: bool = data.get('is_rewatching')
        self.start_date: Optional[datetime] = date(data.get('start_date', None))
        self.finish_date: Optional[datetime] = date(data.get('finish_date', None))
        self.priority: int = data.get('priority')
        self.num_times_rewatched: int = data.get('num_times_rewatched')
        self.rewatch_value: int = data.get('rewatch_value')
        self.tags: List[str] = data.get('tags')
        self.comments: str = data.get('comments')
        self.updated_at: datetime = datetime.fromisoformat(data.get('updated_at'))


class Picture(Nullable):
    __slots__ = ['large', 'medium']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.large: Optional[str] = data.get('large', None)
        self.medium: str = data.get('medium')


class RelatedMediaEdge(Object):
    __slots__ = ['node', 'relation_type', 'relation_type_formatted']

    def __init__(self, data: Dict[str, Any], media_type: Media) -> None:
        super().__init__(data)
        self.media: Media = media_type(data.get('node'))
        self.relation_type: str = data.get('relation_type')
        self.relation_type_formatted: str = data.get('relation_type_formatted')


class Serialization(Object):
    __slots__ = ['id', 'name', 'role']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id = data.get('node').get('id')
        self.name = data.get('node').get('name')
        self.role = data.get('role')


class StartSeason(Nullable):
    __slots__ = ['year', 'season']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.year: int = data.get('year')
        self.season: str = data.get('season')


class Statistics(Nullable):
    __slots__ = ['num_list_users', 'status']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.num_list_users: int = data.get('num_list_users')
        self.status: Status = Status(data.get('status'))


class Status(Object):
    __slots__ = ['watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch']
    
    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.watching: int = data.get('watching')
        self.completed: int = data.get('completed')
        self.on_hold: int = data.get('on_hold')
        self.dropped: int = data.get('dropped')
        self.plan_to_watch: int = data.get('plan_to_watch')


class Studio(Object):
    __slots__ = ['id', 'name']

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')
