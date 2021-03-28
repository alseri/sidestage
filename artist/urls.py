from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_ann/', views.add_ann),
    path('delete_ann/<int:ann_id>/', views.delete_ann),
    path('add_tour/', views.add_tour),
    path('delete_tour/<int:tour_id>/', views.delete_tour),
    path('profile/', views.profile),
    path('profile_edit/', views.edit_profile),
    path('show_new_show/', views.show_new_show),
    path('show_new_show_count/', views.show_new_show_count),
    path('show_new_ann/', views.show_new_ann),

]
