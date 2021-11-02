from django.urls import path, include
from .views import *

urlpatterns = [
    path('hello/', hello, name = 'hello'),
    path('hello/<int:number>', helloNum, name = 'helloNum'),
    path('today/', today, name='today'),
]
