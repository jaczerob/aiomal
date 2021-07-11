from datetime import datetime
from typing import List, Optional


class User:
    def __init__(self, data) -> None:
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.picture: str = data.get('picture')
        self._birthday: str = data.get('birthday')
        self.location: str = data.get('location')
        self._joined_at: str = data.get('joined_at')
        self.anime_statistics: object = data.get('anime_statistics')
        self.time_zone: str = data.get('time_zone')
        self.is_supporter: bool = data.get('is_supporter')

    @property
    def joined_at(self) -> datetime:
        return datetime.fromisoformat(self._joined_at)

    @property
    def birthday(self) -> datetime:
        return datetime.strptime('%Y-%m-%d', self._birthday)


class _Media:
    def __init__(self, data) -> None:
        self.id: int = data.get('id')
        self.title: str = data.get('title')
        self.main_picture: object = data.get('main_picture')
        self.alternative_titles: object = data.get('alternative_titles')
        self.start_date: str = data.get('start_date')
        self.end_date: str = data.get('end_date')
        self.synopsis: str = data.get('synopsis')
        self.mean: Optional[float] = data.get('mean', None)
        self.rank: Optional[int] = data.get('rank', None)
        self.popularity: int = data.get('popularity')
        self.num_list_users: int = data.get('num_list_users')
        self.nsfw: str = data.get('nsfw')
        self.genres: List[object] = data.get('genres')
        self._created_at: str = data.get('created_at')
        self._updated_at: str = data.get('updated_at')
        self.media_type: str = data.get('media_type')
        self.status: str = data.get('status')
        self.my_list_status: Optional[object] = data.get('my_list_status', None)
        self.pictures: List[object] = data.get('pictures')
        self.background: str = data.get('background')
        self.related_anime: List[object] = data.get('related_anime')
        self.related_manga: List[object] = data.get('related_manga')
        self.recommendations: List[object] = data.get('recommendations')

    @property
    def created_at(self) -> datetime:
        return datetime.fromisoformat(self._created_at)

    @property
    def updated_at(self) -> datetime:
        return datetime.fromisoformat(self._updated_at)


class Anime(_Media):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.num_episodes: int = data.get('num_episodes')
        self.start_season: object = data.get('start_season')
        self.broadcast: object = data.get('broadcast')
        self.source: str = data.get('source')
        self.average_episode_duration: int = data.get('average_episode_duration')
        self.rating: int = data.get('rating')
        self.studios: List[object] = data.get('studios')
        self.statistics: object = data.get('statistics')


class Manga(_Media):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.num_volumes: int = data.get('num_volumes')
        self.num_chapters: int = data.get('num_chapters')
        self.authors: List[object] = data.get('authors')
        self.serialization: List[object] = data.get('serialization')
