from celery import shared_task
from music.models import CustomUser
from datetime import datetime
import django
django.setup()

from spotipy.oauth2 import SpotifyOAuth
from music.cachemanager import DatabaseCacheHandler
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = 'http://localhost:8000/',

@shared_task()
def print_users():
    usuarios = CustomUser.objects.all()
    for usuario in usuarios:
        if usuario.verificated:
            print("@@@@@@")
            cache_handler = DatabaseCacheHandler(usuario.id)
            auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:8000/",
            scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing ",
            cache_handler=cache_handler)
            sp = spotipy.Spotify(auth_manager=auth_manager)
            print(datetime.now(), sp.me())
            return 1



'''@shared_task()
def print_current_song():
    pass'''