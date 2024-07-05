import time
from datetime import datetime
from django.conf import settings
import django
from Rolalog.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from music.models import CustomUser
from spotipy.oauth2 import SpotifyOAuth
from music.cachemanager import DatabaseCacheHandler
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = 'http://localhost:8000/'

while True:
    usuarios = CustomUser.objects.all()
    for usuario in usuarios:
        if usuario.verificated:
            cache_handler = DatabaseCacheHandler(usuario.id)
            auth_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://localhost:8000/",
                scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing ",
                cache_handler=cache_handler)
            sp = spotipy.Spotify(auth_manager=auth_manager)
            print(datetime.now(), sp.me())
            time.sleep(15)

