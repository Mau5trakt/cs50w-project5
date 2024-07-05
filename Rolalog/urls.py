"""
URL configuration for Rolalog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from music.views import *


urlpatterns = [
    path('', router, name='router'),
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('callback', callback, name='callback'),
    path('activity', user_notifications, name='notifications'),
    path('user/<str:username>', profile, name='homepage'),
    path('about', about_us, name='about'),
    path('music/', include('music.urls')),
    path('library/<str:username>', library, name='library'),
    path('musicexchange', music_exchange, name='music_exchange'),
    path('musicexchange/create', create_me, name='create_me'),
    path('musicexchange/history', history_me, name='history_me'),
    path('user/<str:username>/latest-report', latest_report, name='latest_report'),

]
