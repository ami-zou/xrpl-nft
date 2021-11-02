from django.shortcuts import render
from django.http import HttpResponse
import datetime

from .forms import *
from .models import *

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


def create(request):
    
    if request.method == 'POST'  and request.FILES['file']:
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.file = request.FILES['file']

            # handles the xrp generation
            file.save()
            mintNFT(file)
            return render(request, "generate.html", {'file' : file})
    else:
        form = UploadFileForm()
        context = {
            'form':form,
        }
    
    #return render(request, 'books_website/UploadBook.html', context)

    return render(request, "create.html", context)

def mintNFT(file):
    #console.log()
    HttpResponse('The file is saved and will now be used to create an NFT on XRPL')