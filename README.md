# aiomal
An asynchronous Python wrapper for the MyAnimeList API, made for use in asynchronous web frameworks such as Sanic or for Discord bots.

This is very early development and not completely functional yet. Any assistance is welcomed greatly.

# Usage

```python
>>> client = Client(client_id, client_secret)
>>> user = client.make_user(access_token, refresh_token)
>>> anime = await user.get_anime_details(anime_id=11757)
>>> print(anime.title, anime.start_date)
Sword Art Online 2012-07-08
```

# TODO
- Finish Documentation
    - Publicly exposed types (maintypes.py, MyListStatus)
- Logging
