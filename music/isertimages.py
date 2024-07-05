import time
from datetime import datetime
from django.conf import settings
import django
from Rolalog.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from music.models import *
from spotipy.oauth2 import SpotifyOAuth
from music.cachemanager import DatabaseCacheHandler
import spotipy
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz
from music.functions import convert_to_desired_format


load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = 'http://localhost:8000/'





cache_handler = DatabaseCacheHandler(1)
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8000/",
    scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
    cache_handler=cache_handler)
sp = spotipy.Spotify(auth_manager=auth_manager)



#print(sp.album('79dL7FLiJFOO0EoehUHQBv'))
print(sp.track('2nVDF64ItzCvVNbAAvQ4UX'))
#print(sp.playlist('1TQM5aHaDaH7jIsM1c2WuI'))


'''historial = sp.current_user_recently_played(limit=50)

songs = historial['items']

for a in songs:
    # track name , timestamp
    date = convert_to_desired_format(a['played_at'])

    timestamp = date
    song_id = a['track']['id']
    song_name = a['track']['name']
    song_album_id = a['track']['album']['id']
    song_album_name = a['track']['album']['name']
    song_artist_id = a['track']['artists'][0]['id']
    song_artist_name = a['track']['artists'][0]['name']
    infoArtist = sp.artist(song_artist_id)
    artistIMG = infoArtist['images'][0]['url']
    song_cover_url = a['track']['album']['images'][0]['url']

    print(date, song_id, song_name, song_album_id, song_album_name, song_artist_id, song_artist_name, artistIMG, song_cover_url)




'''





