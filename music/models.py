from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage



class CustomUser(AbstractUser):
    description = models.CharField(max_length=140)
    image = models.ImageField(upload_to='rolalog-profile-pictures')
    verificated = models.BooleanField(default=False)
    pro = models.BooleanField(default=False)

    class Meta:
        app_label = 'music'




class DatabaseCacheHandling(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    token = models.JSONField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]


class Tracking(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=30)
    is_playing = models.BooleanField(default=True)
    progress = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=30)
    song_name = models.CharField(max_length=300)
    song_album_id = models.CharField(max_length=30)
    song_album_name = models.CharField(max_length=300)
    song_artist_id = models.CharField(max_length=30)
    song_artist_name = models.CharField(max_length=300)
    song_artist_img = models.CharField(max_length=100)
    song_cover_url = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]



class LikedSong(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=30)
    song_name = models.CharField(max_length=300)
    song_album_id = models.CharField(max_length=30)
    song_album_name = models.CharField(max_length=300)
    song_artist_id = models.CharField(max_length=30)
    song_artist_name = models.CharField(max_length=300)
    song_cover_url = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]

class ProfileLog(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='profilelog_user')
    to = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='profilelog_to')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]


class ProfileLogLikes(models.Model):
    log = models.ForeignKey(to=ProfileLog, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)



class Review(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=30)
    text = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]


class ReviewLike(models.Model):
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='follow_user')
    follows = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='following')
    timestamp = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='notification_owner')
    user_from = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='notification_user_from')
    action = models.CharField(max_length=60)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]


class Report(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    period = models.CharField(max_length=23)
    report = models.JSONField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]




class MusicRequest(models.Model):
    # person who makes the request
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='musicrequest_owner')
    #person who receives the request
    to = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='musicrequest_to')
    type = models.CharField(max_length=8)
    item_name = models.CharField(max_length=512)
    item_image_url = models.CharField(max_length=100)
    spotify_link = models.CharField(max_length=255)

    spotify_id = models.CharField(max_length=30)
    status = models.IntegerField()
    # 0: sended, 1 acepted, 2 rejected album track playlist
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]


class MusicResquestSong(models.Model):
    music_request = models.ForeignKey(to=MusicRequest, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=30)
    song_name = models.CharField(max_length=300)
    song_album_id = models.CharField(max_length=30)
    song_album_name = models.CharField(max_length=300)
    song_artist_id = models.CharField(max_length=30)
    song_artist_name = models.CharField(max_length=300)
    song_cover_url = models.CharField(max_length=100)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'])
        ]

class Setting(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    preferences = models.JSONField(null=True)
