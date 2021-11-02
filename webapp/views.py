from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def hello(request):
   # return render(request, "webapp/templates/hello.html", {})
   return HttpResponse("Hello World!")

def helloNum(request, number):
   text = "<h1>welcome to my app number %s!</h1>"% number
   return HttpResponse(text)

def today(request):
    today = "11/02/2021"
    return render(request, "hello.html", {"today" : today})