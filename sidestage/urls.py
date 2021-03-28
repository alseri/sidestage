from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register_artist/', views.register_artist),
    path('register_fan/', views.register_fan),
    path('login/', views.login),
    path('dashboard/artist/', views.dashboard_artist),
    path('dashboard/fan/', views.dashboard_fan),
    path('artists/', views.all_artists),
    path('artists/<int:artist_id>/', views.artist_profile),
    path('artists/<int:artist_id>/rsvp/<int:tour_id>/', views.rsvp),
    path('artists/<int:artist_id>/cancel/<int:tour_id>/', views.cancel),
    path('logout/', views.logout),
]
