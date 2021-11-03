from django.shortcuts import render
from django.http import HttpResponse
import logging

from .forms import *
from .models import *
from webapp.helpers import ipfs
from webapp.helpers import xrpl

# Create your views here.

# General setup
logging.basicConfig(level=logging.INFO)

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
            file.save() #TODO: don't save locally if the name is redundant
            logging.info('The file is saved and will now be used to create an NFT on XRPL')
            # STEP ONE: write metadata (both img link and desc) to IPFS
            file.ipfs_uri = "Not set"
            file.metadata_uri = "Not set"
            data = ipfs.write_metadata(file)

            # STEP TWO: mint XRP NFT
            data = xrpl.mint_nft(data)
            return render(request, "generate.html", {'data' : data})
    else:
        form = UploadFileForm()
        context = {
            'form':form,
        }
    
    #return render(request, 'books_website/UploadBook.html', context)

    return render(request, "create.html", context)

        
