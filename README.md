# aiomal
An asynchronous Python wrapper for the MyAnimeList API, made for use in asynchronous web frameworks such as Sanic or for Discord bots.

# Usage

Make a developer application on the MyAnimeList website and obtain your Client ID and Client Secret. These are necessary to obtain access to the MyAnimeList API.

```python
>>> client = Client(client_id, client_secret)
>>> auth_url = client.generate_auth_url()
>>> # Send auth URL to a user and obtain auth code from it from the pingback URL set in your apiconfig

...

>>> code_verifier = secrets.get_new_code_verifier()
>>> access_token, refresh_token = client.generate_access_token(auth_code, code_verifier)
>>> user = client.make_user(access_token, refresh_token)
>>> anime = await user.get_anime_details(anime_id=11757)
>>> print(anime.title, anime.start_date)
Sword Art Online 2012-07-08
```

# TODO
- Finish Documentation
    - Publicly exposed types (maintypes.py, MyListStatus)
