from django.urls import path
from . import views

urlpatterns = [
    path('ats/', views.ats, name='ats'), # auto tracking song
    path('flibrary/',  views.f_library, name='flibrary'),
    path('fusername/', views.f_username, name='fusername'),
    path('fsearch/', views.f_search, name='fsearch'),
    path('fcreateME/', views.f_MErequest, name='fmeRequest'),
    path('request/<int:id>', views.request_element, name='request_element'),
    path('fmanageRequests/', views.manage_request, name='manage_request'),
    #path('')
    ]
