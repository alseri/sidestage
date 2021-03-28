from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('show_new_show_count_fan/', views.show_new_show_count_fan),
    path('follow/<int:artist_id>/', views.follow_artist),
    path('like/<int:ann_id>/', views.like_ann, name='like'),
    path('rewards/', views.rewards_refresh),
]
