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
                scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
                cache_handler=cache_handler)
            sp = spotipy.Spotify(auth_manager=auth_manager)
            song = sp.current_user_playing_track()

            if song is None or song['currently_playing_type'] != 'track':
                print(f'{usuario} is not playing')
            else:
                print(song)
                playing = song['is_playing']

                actprog = song['progress_ms']
                duration = song['item']['duration_ms']

                print(actprog, duration)
                #print(round(actprog/duration, 2))
                #print(round(actprog/duration, 1))

                name = song['item']['name']
                artist = song['item']['artists'][0]['name']
                artist_id = song['item']['artists'][0]['id']

                infoArtist = sp.artist(artist_id)
                artistIMG = infoArtist['images'][0]['url']


                song_id = song['item']['id']
                album_name = song['item']['album']['name']
                album_id = song['item']['album']['id']
                song_cover = song['item']['album']['images'][0]['url']
                print(f'{usuario} is playing ({playing}): "{name}" by "{artist}" length:  {duration}  id: {song_id}')

                # Create the Tracking object for the user
                Tracking.objects.create(user=usuario, song_id=song_id, is_playing=playing, progress=round(actprog/duration, 2))
                last_song = History.objects.filter(user=usuario).first()

                if last_song:
                    if actprog >= round(duration / 2) and name != last_song.song_name:
                        History.objects.create(
                            user=usuario,
                            song_id=song_id,
                            song_name=name,
                            song_album_id=album_id,
                            song_album_name=album_name,
                            song_artist_id=artist_id,
                            song_artist_name=artist,
                            song_cover_url=song_cover,
                            song_artist_img=artistIMG
                        )
                else:

                    historial = sp.current_user_recently_played(limit=50)

                    songs = historial['items']

                    for a in songs:
                        # track name , timestamp
                        song_id = a['track']['id']
                        song_name = a['track']['name']
                        song_album_id = a['track']['album']['id']
                        song_album_name = a['track']['album']['name']
                        song_artist_id = a['track']['artists'][0]['id']
                        song_artist_name = a['track']['artists'][0]['name']
                        infoArtist = sp.artist(song_artist_id)
                        artistIMG = infoArtist['images'][0]['url']
                        song_cover_url = a['track']['album']['images'][0]['url']
                        History.objects.create(user=usuario,
                                               song_id=song_id,
                                               song_name=song_name,
                                               song_album_id=song_album_id,
                                               song_album_name=song_album_name,
                                               song_artist_id=song_artist_id,
                                               song_artist_name=song_artist_name,
                                               song_cover_url=song_cover_url,
                                               song_artist_img=artistIMG)

                    History.objects.create(
                        user=usuario,
                        song_id=song_id,
                        song_name=name,
                        song_album_id=album_id,
                        song_album_name=album_name,
                        song_artist_id=artist_id,
                        song_artist_name=artist,
                        song_cover_url=song_cover,
                        song_artist_img=artistIMG
                    )
    time.sleep(20)

