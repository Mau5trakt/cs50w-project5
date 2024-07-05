from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'description', 'image', 'verificated', 'pro', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

    # Campos que se pueden buscar en la lista de usuarios
    search_fields = ['username', 'email', 'first_name', 'last_name']

    # Detalles de cómo se muestra el usuario en la vista de detalle
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'email', 'description', 'image', 'verificated', 'pro')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos adicionales para mostrar en el formulario de detalle del usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'description', 'image',
                       'verificated', 'pro', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Configura cómo se ordena la lista de usuarios
    ordering = ('username',)


# Register your models here.


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user',  'song_id', 'song_name', 'song_album_id', 'song_album_name',
                    'song_artist_id', 'song_artist_name', 'song_artist_img',     'song_cover_url']


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'song_id', 'is_playing', 'progress']


@admin.register(DatabaseCacheHandling)
class CacheHandling(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'token']

@admin.register(MusicRequest)
class MusicRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'to', 'type', 'spotify_id', 'status', 'timestamp']

@admin.register(MusicResquestSong)
class MRSADMIN(admin.ModelAdmin):
    list_display = ['id', 'music_request', 'song_id', 'song_name', 'liked', 'timestamp']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'user_from', 'action', 'timestamp']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'period', 'report', 'timestamp']