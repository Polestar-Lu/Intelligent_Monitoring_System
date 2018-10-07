from django.contrib import admin
from django.urls import path, include, re_path
from Intelligent_Monitoring_System.settings import MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
    path('account/', include('Account.urls')),
    path('video/', include('Video.urls')),
    re_path(r'media/img/(?P<path>.*)$', serve, {"document_root": (MEDIA_ROOT + '/img')}),
]
