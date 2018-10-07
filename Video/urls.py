from django.contrib import admin
from django.urls import path, include


from . import views
urlpatterns = [
    path('video_setting/', views.setting),
    path('index/', views.index),
    path('video/', views.play_video),
    path('face_1/', views.face_1),
    path('face_2/', views.face_2),
    path('face_3/', views.face_3),
    path('face_4/', views.face_4),
    path('face_5/', views.face_5),
    path('message/', views.show_message),
]