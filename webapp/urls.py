from django.urls import re_path as url
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 

urlpatterns = [
    path('hello/', hello, name = 'hello'),
    path('hello/<int:number>', helloNum, name = 'helloNum'),
    path('today/', today, name='today'),
    path('create/', create, name='create'),
    path('create/mint', mint, name='mint'),
    # path('create/mint', mintData, name='mint'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL)
