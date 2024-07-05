import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core import serializers
from .models import *
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, user_logged_in
from .cachemanager import DatabaseCacheHandler
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import connection
from .rlquerys import *
from django.core.paginator import Paginator


load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = 'http://localhost:8000/'
# Create your views here.


def register(request):
    if request.POST:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
        confirmation = request.POST['confirmation']


        dbmail = CustomUser.objects.filter(email__iexact=mail).first()
        dbuser = CustomUser.objects.filter(username__iexact=username).first()

        if not username:
            messages.error(request, "Must provide an username")
        if not mail:
            messages.error(request, "Must provide an valid email")
        if not password:
            messages.error(request, "Must provide an password")
        if not confirmation:
            messages.error(request, "Must provide an confirmation")
        if confirmation != password:
            messages.error(request,"Password and confirmation doesn't match")
        if dbmail is not None:
            messages.error(request,"Email already in use")
        if dbuser is not None:
            messages.error(request, "Username already in use")


        CustomUser.objects.create(
            username=username,
            password=make_password(password),
            email=mail,
        )
        request.session['username'] = username
        return redirect('login')

    return render(request, 'music/register.html')


def user_login(request):

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        current_user = CustomUser.objects.filter(username__iexact=username).first()
        if current_user is None:
            messages.error(request,"Error Username")

        #if not current_user.verificated:

        #    msg = "Your account wasn't verificated by the admin yet"
        #    return render(request, 'music/errors.html', {'msg': msg, 'code':401 })

        if not username:
            messages.error(request,"Must provide an username")
        if not password:
            messages.error(request, 'Must provide an password')

        user = authenticate(request, username=current_user.username, password=password)
        if user is not None:
            login(request, user)
            print('se autentica')
            request.session['username'] = current_user.username
            request.session['user_id'] = current_user.id

            return redirect('notifications')


        messages.error(request, 'Invalid Username/Password')

    return render(request, 'music/login.html')



def profile(request, username):

    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    current_user = CustomUser.objects.filter(username__iexact=username).first()

    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass



    if current_user is None:
        msg = "This user isn't with us, yet"
        return render(request, 'music/errors.html', {'msg': msg, 'code': 404, 'to': to})

    latest_history = History.objects.filter(user=current_user).order_by('-timestamp')[:10]


    artists_count = History.objects.filter(user=current_user).aggregate(Count('song_artist_name', distinct=True))['song_artist_name__count']
    rolls = History.objects.filter(user=current_user).aggregate(Count('song_name', distinct=False))['song_name__count']

    now = timezone.now()
    last_week = now - timedelta(days=7)

    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_week = last_week.replace(hour=0, minute=0, second=0, microsecond=0)

     #Calcular el último viernes a las 00:00:00 h
    last_friday = now - timedelta(days=(now.weekday() + 3) % 7)
    last_friday = last_friday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcular el siguiente jueves a las 23:59:59 h
    next_thursday = last_friday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    last_friday_str = last_friday.strftime('%Y-%m-%d %H:%M:%S')
    next_thursday_str = next_thursday.strftime('%Y-%m-%d %H:%M:%S')
    hoy = datetime.now()
    semanaatras = datetime.now() - timedelta(days=7)
    print(last_friday, next_thursday)
    print('GGG', now, last_week)

    with connection.cursor() as cursor:
        cursor.execute('''
              SELECT COUNT(*)
                FROM music_history
                WHERE user_id = %s
                AND timestamp BETWEEN %s AND %s;
          ''', [current_user.id, last_friday, next_thursday])
        result = cursor.fetchone()


    weekly_rolls = result[0]

    top_albums = queryprofile_weekly('song_album_name', current_user.id, True, semanaatras, hoy)
    top_artists = queryprofile_weekly('song_artist_name', current_user.id, True, semanaatras, hoy)
    top_songs = queryprofile_weekly('song_name', current_user.id, True, semanaatras, hoy)

    return render(request, 'music/profile.html', {'user': current_user, 'to': to, 'loged': loged,  'image': image, 'history': latest_history, 'artists': artists_count, 'rolls': rolls, 'weekly_rolls': weekly_rolls,  "albums": top_albums, 'top_artists': top_artists, 'top_songs': top_songs})

@require_POST
def ats(request):
    data = json.load(request)
    current_user = CustomUser.objects.filter(username__iexact=data['username']).first()
    latest_history = History.objects.filter(user=current_user).order_by('-timestamp')[:10]

    tmp_json = serializers.serialize('json', latest_history)
    tmp_obj = json.loads(tmp_json)

    cache_handler = DatabaseCacheHandler(current_user.id)
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing ",
        cache_handler=cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    song = sp.current_user_playing_track()

    if song is None or song['currently_playing_type'] != 'track':
        return JsonResponse({'status': 'not_playing'})
    else:
        print(song)

    print(data)

    return JsonResponse({'status': 'playing', 'playing': song,'history': tmp_obj, 'none': None})

@require_POST
def f_library(request):
    data = json.load(request)
    print(data)
    current_user = CustomUser.objects.filter(username__iexact=data['username']).first()

    valids = ['rolls', 'albums', 'artists', 'songs']
    if data['type'] not in valids:
        return JsonResponse({"ALERT": "NOT VALID"})


    if data['type'] == 'rolls':
        # validate the page is a str

        history = History.objects.all().filter(user_id=current_user)
        paginator = Paginator(history, 50)
        page_obj = paginator.get_page(data['page'])
        pagerange = paginator.num_pages

        tmp_json = serializers.serialize('json', page_obj)
        tmp_obj = json.loads(tmp_json)

        return JsonResponse({'objects': tmp_obj,  'pages': pagerange, 'qty': paginator.count}, safe=False)

    else:
        # valids = ['rolls', 'albums', 'artists', 'songs']

        tables = {
            'albums': 'song_album_name',
            'artists': 'song_artist_name',
            'songs': 'song_name'
        }

            #data['type'] == 'albums':

        '''
        WORK ON THE LOGIC TO RETURN THE ALBUMS (and everything)
        
        -> ESPECTED 1. - IMG - ALBUM NAME - ARTIST NAME - QTY ROLLS
        
        ITS THE SAME QUERY OF THE PROFILE BUT WITHOUT LIMIT
        SO IM GONNA WORK THAT WAY
        
        '''
        elements = queryprofile(tables[data['type']], current_user.id, False)
        #albums = queryprofile('song_album_name', current_user.id, False)
        paginator = Paginator(elements, 50)
        page_obj = paginator.get_page(data['page'])
        pagerange = paginator.num_pages

        # print(page_obj)

        #tmp_json = serializers.serialize('json', page_obj, fields='h.song_album_name')
        #print(tmp_json)
        # tmp_obj = json.loads(tmp_json)

        return JsonResponse({'objects': list(page_obj), 'pages': pagerange, 'qty': paginator.count}, safe=False)


@login_required()
def music_exchange(request):
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()
    music_requests = MusicRequest.objects.filter(to=current_user, status=0)
    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass

    print(current_user.username)


    return render(request, 'music/musicexchange.html', {'user': current_user, 'to': to, 'image': image, 'loged': loged, 'requests':  music_requests})



@login_required
def create_me(request):
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()

    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass

    print(current_user.username)


    return render(request, 'music/createME.html', {'user': current_user, 'to': to, 'image': image, 'loged': loged})


@login_required()
def history_me(request):
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()

    to = '/music/login'
    loged = False

    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass

    sended = MusicRequest.objects.filter(owner=current_user)
    accepted = MusicRequest.objects.filter(to=current_user, status=1)
    #acepted = MusicRequest.objects.filter(to=current_user, status=)


    return render(request, 'music/historyME.html', {'user': current_user, 'to': to, 'loged': loged, 'sended': sended, 'accepted': accepted, 'image': image})


@login_required()
def request_element(request, id):
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()
    current_request = MusicRequest.objects.filter(id=id).first()
    #validaation if the request exists
    #validation if is the owner or the receiver

    to = '/music/login'
    loged = False

    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True



    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass

    auth = False
    if current_user.username == current_request.to.username or current_user.username == current_request.owner.username:
        auth = True

    if current_request is None or not auth:
        print(auth)
        return render(request, 'music/errors.html', {'msg': 'Invalid request', 'code': 404, 'to':to})

    music_elements = MusicResquestSong.objects.filter(music_request=current_request.id)



    return render(request, 'music/requestElement.html', {'user': current_user, 'to': to, 'loged': loged, 'image': image, 'songs': music_elements, 'request': current_request})




@login_required
@require_POST
def f_username(request):
    data = json.load(request)
    print(data)
    user_fetched = CustomUser.objects.filter(username__iexact=data['username']).first()

    return JsonResponse({'user_exists': True if user_fetched else False})


@login_required
@require_POST
def manage_request(request):
    data = json.load(request)
    print(data)

    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()

    music_request = MusicRequest.objects.filter(id=data['id']).first()

    print(music_request.to, current_user.username)
    print(type(music_request.to.username), type(current_user.username))

    if music_request.to.username == current_user.username:

        print('entra')

        if data['action'] == 'accept':
            music_request.status = 1
            music_request.save()


        elif data['action'] == 'reject':
            music_request.status = 2
            music_request.save()

        return JsonResponse({'status': 'done'})

    return JsonResponse({'status': 'error'})






@login_required
@require_POST
def f_MErequest(request):
    data = json.load(request)

    valids = ['playlist', 'album', 'track']


    print(data)

    destination_user = CustomUser.objects.filter(username__iexact=data['to']).first()
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()

    print(f'requested by {current_user.username} to: {destination_user.username}')

    if destination_user.username == current_user.username or data['type'] not in valids:
        return JsonResponse({'status': 'failed'})



    cache_handler = DatabaseCacheHandler(current_user.id)
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing ",
        cache_handler=cache_handler,
    )
    sp = spotipy.Spotify(auth_manager=auth_manager, retries=50, backoff_factor=0.3)

    e_image = ''
    e_name = ''
    e_link = ''

    # Do the comprobation here
    if data['type'] == 'playlist':
        playlist = sp.playlist(data['sp_id'])

        e_image = playlist['images'][0]['url']
        e_name = playlist['name']
        e_link = playlist['external_urls']['spotify']

        # image and name and link
    elif data['type'] == 'album':
        album = sp.album(data['sp_id'])

        e_image = album['images'][0]['url']
        e_name = album['name']
        e_link = album['external_urls']['spotify']

    elif data['type'] == 'track':
        track = sp.track(data['sp_id'])

        e_image = track['album']['images'][0]['url']
        e_name = track['name']
        e_link = track['external_urls']['spotify']


    music_request = MusicRequest.objects.create(
        owner=current_user,
        to=destination_user,
        type=data['type'],
        spotify_id=data['sp_id'],
        item_name=e_name,
        item_image_url=e_image,
        spotify_link=e_link,
        status=0
    )

    notification = Notification.objects.create(
        owner=destination_user,
        user_from=current_user,
        action=f'Requested you to listen {e_name}'
    )

    print('music request #:', music_request.id)
    #  es con create mrs = MusicRequest.objects.filter()
    try:
        if data['type'] == 'playlist':
            playlist = sp.playlist(data['sp_id'])
            for song in playlist['tracks']['items']:
                if song['track']['track']:
                    MusicResquestSong.objects.create(
                        music_request=music_request,
                        song_id=song['track']['id'],
                        song_name=song['track']['name'],
                        song_album_id=song['track']['album']['id'],
                        song_album_name=song['track']['album']['name'],
                        song_artist_id=song['track']['artists'][0]['id'],
                        song_artist_name=song['track']['artists'][0]['name'],
                        song_cover_url=song['track']['album']['images'][0]['url'],
                        liked=False
                        )
        elif data['type'] == 'album':
            print('in album')
            album = sp.album(data['sp_id'])
            album_id = album['id']
            album_name = album['name']
            image = album['images'][0]['url']
            artist_name = album['artists'][0]['name']
            artist_id = album['artists'][0]['id']

            for song in album['tracks']['items']:
                MusicResquestSong.objects.create(
                    music_request=music_request,
                    song_id=song['id'],
                    song_name=song['name'],
                    song_album_id=album_id,
                    song_album_name=album_name,
                    song_artist_id=artist_id,
                    song_artist_name=artist_name,
                    song_cover_url=image,
                    liked=False
                )
                print('created album ')

        elif data['type'] == 'track':
            track = sp.track(data['sp_id'])
            MusicResquestSong.objects.create(
                music_request=music_request,
                song_id=track['id'],
                song_name=track['name'],
                song_album_id=track['album']['id'],
                song_album_name=track['album']['name'],
                song_artist_id=track['artists'][0]['id'],
                song_artist_name=track['artists'][0]['name'],
                song_cover_url=track['album']['images'][0]['url'],
                liked=False
            )
            print('created_song')
        return JsonResponse({'status': 'done'})
    except:
        return JsonResponse({'status': 'error'})


@login_required
@require_POST
def f_search(request):
    cache_handler = DatabaseCacheHandler(request.session['user_id'])
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/callback",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
        cache_handler=cache_handler
        # Adjust scope based on your requirements
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    data = json.load(request)
    print(data)

    search = sp.search(data['search'], type='track,album,playlist', limit=50)


    return JsonResponse({'results': search})

def latest_report(request, username):

    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    owner = CustomUser.objects.filter(username__iexact=username).first()
    try:
        actual_report = Report.objects.filter(user=owner).first()
        print(actual_report.report)
    except:
        return render(request, 'music/errors.html', {'msg': "Whoops, this user doesn't  have a report yet. Wait till the next friday", 'to': to})

    if actual_report is None:
        render(request, 'music/errors.html', {'msg': "Whoops, this user doesn't  have a report, try the next friday"})

    days = actual_report.report['roll_log']['days']

    print(days)


    return render(request, 'music/report.html', {'loged': loged,  'report_info': actual_report, 'report': actual_report.report, 'days': days,'to':to})



def callback(request):
    cache_handler = DatabaseCacheHandler(request.session['user_id'])
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/callback",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
        cache_handler=cache_handler
        # Adjust scope based on your requirements
    )
    code = request.GET.get('code')
    if code:
        print('hay codigo')
        auth_manager.get_access_token(code)



    else:
        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            auth_url = auth_manager.get_authorize_url()
            print('redirigiendo a la url de spotify')
            return redirect(auth_url)



    print('llega hasta el final')
    current_user = CustomUser.objects.filter(id=request.session.get('user_id')).first()
    print(f"authenticated: {current_user.verificated}")

    cache_handler = DatabaseCacheHandler(request.session['user_id'])
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/callback",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
        cache_handler=cache_handler)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    try:
        print(sp.me())
    except:
        return render(request, 'music/errors.html', {'msg': 'No se ha autorizado'})

    return redirect('notifications')


def library(request, username):
    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    current_user = CustomUser.objects.filter(username__iexact=username).first()

    image = False
    try:
        print(current_user.image)
        print(current_user.image.url)
        image = True
    except:
        pass

    if current_user is None:
        msg = "This user isn't with us, yet"
        return render(request, 'music/errors.html', {'msg': msg, 'code': 404, 'to': to})




    return render(request, 'music/library.html',{'user': current_user, 'to': to, 'image': image, 'loged': loged})



@login_required
def user_notifications(request):
    current_user = CustomUser.objects.filter(id=request.session['user_id']).first()
    notifications = Notification.objects.filter(owner=current_user)
    #manage if the user is verified user.verified
    to = f'/user/{request.session['username']}'

    cache_handler = DatabaseCacheHandler(request.session['user_id'])


    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8000/callback",
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played",
        cache_handler=cache_handler)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    try:
        print(sp.me())
    except:
        return render(request, 'music/errors.html', {'msg':  'No se ha autorizado'})
    print("In Notifications")

    return render(request, 'music/notifications.html', {'user': request.session.get('username'), 'to':to, 'loged': True, 'notifications': notifications})



def router(request):

    if request.user.is_authenticated:
        return redirect('notifications')
    else:
        return redirect('login')



def about_us(request):
    to = '/music/login'
    loged = False
    if request.user.is_authenticated:
        to = f'/user/{request.session.get('username', '')}'
        loged = True

    return render(request, 'music/aboutus.html', {'loged': loged, 'to': to})


def user_logout(request):
    logout(request)
    return redirect('login')






