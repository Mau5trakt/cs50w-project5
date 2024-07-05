from django.db import connection
from django.conf import settings
import django
#from Rolalog.settings import DATABASES, INSTALLED_APPS
#settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
#django.setup()



rlq_profile_albums = """
    SELECT
    h.song_album_name,
    h.song_id,
    h.song_name,
    h.song_artist_img,
    h.song_album_id,
    h.song_album_name,
    h.song_artist_id,
    h.song_artist_name,
    h.song_cover_url,
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
ORDER BY
    count_table.count DESC,
    count_table.song_album_name
LIMIT 5
"""


rlq_profile_artists = """
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
ORDER BY
    count_table.count DESC,
    count_table.song_artist_name
LIMIT 5
"""

def queryprofile(field, id, limit):
    query = f"""
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
    count_table.count
FROM
    music_history h
JOIN
    (SELECT
        {field},
        MIN(id) as min_id,
        COUNT(*) as count
     FROM
        music_history
     WHERE
        user_id = %s
     GROUP BY
        {field}) count_table
ON
    h.{field} = count_table.{field}
    AND h.id = count_table.min_id
WHERE
    h.user_id = %s
ORDER BY
    count_table.count DESC,
    count_table.{field}


"""
    if limit:
        query += ' LIMIT 5'

    with connection.cursor() as cursor:
        cursor.execute(query, [id, id])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        return [dict(zip(columns, row)) for row in result]



def queryprofile_weekly(field, id, limit, start, end):
    query = f"""
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
        {field},
        MIN(id) as min_id,
        COUNT(*) as count
     FROM
        music_history
     WHERE
        user_id = %s
     GROUP BY
        {field}) count_table
ON
    h.{field} = count_table.{field}
    AND h.id = count_table.min_id
WHERE
    h.user_id = %s
    AND timestamp BETWEEN '{start}' AND '{end}'
    
ORDER BY
    count_table.count DESC,
    count_table.{field}
    


"""
    if limit:
        query += ' LIMIT 5'

    with connection.cursor() as cursor:
        cursor.execute(query, [id, id])
        head = cursor.description
        result = cursor.fetchall()
        columns = [col[0] for col in head]
        return [dict(zip(columns, row)) for row in result]







a = queryprofile('song_album_name', 1, True)
b = queryprofile('song_artist_name', 1, True)



print(a)
print(b)