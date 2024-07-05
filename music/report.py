# This script gotta be run thursday at 23:59:00
from django.db import connection
from django.conf import settings
import django
from Rolalog.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()
from django.utils import timezone
import datetime
from music.models import *

# r = Report.objects.create(user=yoni, period='2024-06-28 2024-07-05', report={'period': {'from': datetime.datetime(2024, 6, 28, 0, 0, tzinfo=datetime.timezone.utc), 'to': datetime.datetime(2024, 7, 5, 0, 0, tzinfo=datetime.timezone.utc)}, 'roll_log': {'qty': 491, 'days': [(datetime.datetime(2024, 6, 30, 0, 0, tzinfo=datetime.timezone.utc), 'Sunday   ', 123), (datetime.datetime(2024, 7, 1, 0, 0, tzinfo=datetime.timezone.utc), 'Monday   ', 59), (datetime.datetime(2024, 7, 2, 0, 0, tzinfo=datetime.timezone.utc), 'Tuesday  ', 137), (datetime.datetime(2024, 7, 3, 0, 0, tzinfo=datetime.timezone.utc), 'Wednesday', 90), (datetime.datetime(2024, 7, 4, 0, 0, tzinfo=datetime.timezone.utc), 'Thursday ', 82)]}, 'main_summary': {'songs': 421, 'albums': 134, 'artists': 85}, 'albums_summary': {'top_album_info': {'name': 'BRAT', 'cover_url': 'https://i.scdn.co/image/ab67616d0000b27388e3822cccfb8f2832c70c2e'}, 'top_albums': ["Melody's Echo Chamber", 'ASTROWORLD', 'OFFLINE!', 'Veteran']}, 'artists_summary': {'top_artist_info': {'name': 'Charli xcx', 'cover_url': 'https://i.scdn.co/image/ab6761610000e5eb936885667ef44c306483c838'}, 'top_artists': ['JPEGMAFIA', 'BROCKHAMPTON', 'Travis Scott', "Melody's Echo Chamber"]}, 'tracks_summary': {'top_track_info': {'name': '360', 'cover_url': 'https://i.scdn.co/image/ab67616d0000b27388e3822cccfb8f2832c70c2e'}, 'top_tracks': ['I Follow You', 'I think about it all the time', 'Mean girls', 'Some Time Alone, Alone']}, 'details': {'avg': 98, 'max_day': 'Tuesday  ', 'max_day_qty': 137, 'min_day': 'Monday   ', 'min_day_qty': 59}})
from datetime import datetime, timedelta

thursday = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

#thursday = thursday - timedelta(days=1)
past_friday = thursday - timedelta(days=7, hours=00, minutes=00)
print(thursday, past_friday)
print(str(thursday.strftime("%Y-%m-%d")), str(past_friday.strftime("%Y-%m-%d")))
#period = str(thursday.strftime("%Y-%m-%d")) +' '+ str(past_friday.strftime("%Y-%m-%d"))
period = str(past_friday.strftime("%Y-%m-%d")) +' '+ str(thursday.strftime("%Y-%m-%d"))


print("#####", period)


def make_report(user_id):
    #2024-06-28 2024-07-05
    # cuantity
    # start 2024-06-28 00:00:00+00:00
    # end 2024-07-05 00:00:00+00:00

    with connection.cursor() as cursor:
        cursor.execute('''
            select COUNT(user_id) from music_history
            WHERE user_id = %s
            AND timestamp BETWEEN %s AND %s;
    
        ''',[user_id, past_friday, thursday])
        result = cursor.fetchone()

        weekly_qty = result[0]

    print(weekly_qty)

    with connection.cursor() as cursor:
        cursor.execute(''' 
        SELECT
        DATE_TRUNC('day', timestamp) AS day,
         TO_CHAR(DATE_TRUNC('day', timestamp), 'Day') AS day_name,
        COUNT(*) AS count
    FROM
        music_history
    WHERE
        user_id = %s
        AND timestamp BETWEEN %s AND %s
        GROUP BY
        day,
        day_name
    ORDER BY
        day;
        
        ''', [user_id, past_friday, thursday])

        result = cursor.fetchall()
        head = cursor.description
        columns = [col[0] for col in head]
        qdays = [dict(zip(columns, row)) for row in result]

    qdays = [{'day': str(d['day']), 'day_name': d['day_name'], 'count': d['count']} for d in qdays]

    print('@@@@', qdays)



    days = {dia.strip(): valor for _, dia, valor in qdays}

    print(days)


    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT song_id) AS qty_song
            FROM music_history
            WHERE user_id = %s AND timestamp BETWEEN %s AND %s;
        ''',[user_id, past_friday, thursday])
        result = cursor.fetchone()

        qty_songs = result[0]

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT song_album_id) AS qty_albums
            FROM music_history
            WHERE user_id = %s AND timestamp BETWEEN %s AND %s;
        ''',[user_id, past_friday, thursday])
        result = cursor.fetchone()

        qty_albums = result[0]

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT song_artist_id) AS qty_artists
            FROM music_history
            WHERE user_id = %s AND timestamp BETWEEN %s AND %s;
        ''',[user_id, past_friday, thursday])
        result = cursor.fetchone()

        qty_artists = result[0]


    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT
        h.song_album_name,
        h.song_id,
        h.song_name,
        h.song_album_id,
        h.song_album_name,
        h.song_artist_id,
        h.song_artist_name,
        h.song_cover_url,
        h.song_artist_img,
        h.timestamp,
        count_table.count
    FROM
        music_history h
    JOIN
        (SELECT
            song_name,
            MIN(id) as min_id,
            COUNT(*) as count
         FROM
            music_history
         WHERE
            user_id =%s
         GROUP BY
            song_name) count_table
    ON
        h.song_name = count_table.song_name
        AND h.id = count_table.min_id
    WHERE
        h.user_id = %s
        AND timestamp BETWEEN %s AND %s
    ORDER BY
        count_table.count DESC,
        count_table.song_name
    limit 5;
        ''',[user_id,user_id, past_friday, thursday])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        top_tracks = [dict(zip(columns, row)) for row in result]

    print('ERROR HERE',top_tracks)




    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT
        h.song_album_name,
        h.song_id,
        h.song_name,
        h.song_album_id,
        h.song_album_name,
        h.song_artist_id,
        h.song_artist_name,
        h.song_cover_url,
        h.song_artist_img,
        h.timestamp,
        count_table.count
    FROM
        music_history h
    JOIN
        (SELECT
            song_album_name,
            MIN(id) as min_id,
            COUNT(*) as count
         FROM
            music_history
         WHERE
            user_id = %s
         GROUP BY
            song_album_name) count_table
    ON
        h.song_album_name = count_table.song_album_name
        AND h.id = count_table.min_id
    WHERE
        h.user_id = %s
        AND timestamp BETWEEN %s AND %s
    ORDER BY
        count_table.count DESC,
        count_table.song_album_name
    limit 5;
        ''',[user_id, user_id,past_friday, thursday])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        top_albums = [dict(zip(columns, row)) for row in result]

    print("###", top_albums)

    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT
        h.song_album_name,
        h.song_id,
        h.song_name,
        h.song_album_id,
        h.song_album_name,
        h.song_artist_id,
        h.song_artist_name,
        h.song_cover_url,
        h.song_artist_img,
        h.timestamp,
        count_table.count
    FROM
        music_history h
    JOIN
        (SELECT
            song_artist_name,
            MIN(id) as min_id,
            COUNT(*) as count
         FROM
            music_history
         WHERE
            user_id = %s
         GROUP BY
            song_artist_name) count_table
    ON
        h.song_artist_name = count_table.song_artist_name
        AND h.id = count_table.min_id
    WHERE
        h.user_id = %s
        AND timestamp BETWEEN %s AND %s
    ORDER BY
        count_table.count DESC,
        count_table.song_artist_name
    limit 5;
        ''',[user_id,user_id,past_friday, thursday])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        top_artists = [dict(zip(columns, row)) for row in result]

    print("###", top_artists)

    with connection.cursor() as cursor:
        cursor.execute('''
        WITH counts_per_day AS (
        SELECT
            DATE_TRUNC('day', timestamp) AS day,
            TO_CHAR(DATE_TRUNC('day', timestamp), 'Day') AS day_name,
            COUNT(*) AS count
        FROM
            music_history
        WHERE
            user_id = %s
            AND timestamp BETWEEN %s AND %s
        GROUP BY
            day,
            day_name
    )
    SELECT
        (SELECT MIN(count) FROM counts_per_day) AS min_count,
        (SELECT TO_CHAR(day, 'Day') FROM counts_per_day WHERE count = (SELECT MIN(count) FROM counts_per_day)) AS day_min_count,
        (SELECT MAX(count) FROM counts_per_day) AS max_count,
        (SELECT TO_CHAR(day, 'Day') FROM counts_per_day WHERE count = (SELECT MAX(count) FROM counts_per_day)) AS day_max_count,
        ROUND(AVG(count))::INT AS avg_count
    FROM
        counts_per_day;
        
        ''',[user_id,past_friday, thursday])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        details = [dict(zip(columns, row)) for row in result]

    print(details)
    details = details[0]


    """
    {report: roll_log :{
        
        }
      } 
    
    """
    #albums_list = [a['song_album_name'] for a in top_albums[1:]]
    #tracks_list = [a['song_name'] for a in top_tracks[1:]]
    #tracks_list = [a['song_name'] for a in top_tracks[1:]]



    report = {
          'period':{
              'from':str(past_friday),
               'to': str(thursday)
          },
          "roll_log":{
             "qty":weekly_qty,
             "days":qdays,
          },
          "main_summary":{
             "songs":qty_songs,
             "albums":qty_albums,
             "artists":qty_artists
          },
          "albums_summary":{
             "top_album_info":{
                "name":top_albums[0]['song_album_name'],
                "cover_url":top_albums[0]['song_cover_url'],
                 "qty":top_albums[0]['count']
             },
             "top_albums":[{'name': album['song_album_name'], 'count': album['count']} for album in top_albums[1:]]

          },
          "artists_summary":{
             "top_artist_info":{
                "name":top_artists[0]['song_artist_name'],
                "cover_url":top_artists[0]['song_artist_img'],
                "qty":top_artists[0]['count']
             },
             "top_artists":[{'name': artist['song_artist_name'], 'count': artist['count']} for artist in top_artists[1:]]
          },
          "tracks_summary":{
             "top_track_info":{
                "name":top_tracks[0]['song_name'],
                "cover_url":top_tracks[0]['song_cover_url'],
                "qty":top_tracks[0]['count']
             },
             "top_tracks":[{'name': track['song_name'], 'count': track['count']} for track in top_tracks[1:]]

          },
          "details":{
             "avg":details['avg_count'],
             "max_day":details['day_max_count'],
             "max_day_qty":details['max_count'],
             "min_day":details['day_min_count'],
             "min_day_qty":details['min_count']
          }
       }


    print(report)



    person = CustomUser.objects.filter(id=user_id).first()
    print(top_albums)
    new_report = Report.objects.create(user=person, period=period, report=report)
    result = [{'name': album['song_album_name'], 'count': album['count']} for album in top_albums[1:]]
    print('the report', report)
    print(result)

#FOR ALL ACTIVES
make_report(9)

people = CustomUser.objects.all()

for p in people:
    if p.verificated:
        make_report(p.id)