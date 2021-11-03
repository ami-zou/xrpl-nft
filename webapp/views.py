from django.shortcuts import render
from django.http import HttpResponse
import datetime
import logging
import requests
from django.conf import settings
from pathlib import Path
import os
from metadata import sample_metadata
from media import *
import json

from .forms import *
from .models import *

# Create your views here.

# General setup
logging.basicConfig(level=logging.INFO)
ipfs_url = "http://localhost:5001"

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
            data = write_metadata(file)

            # STEP TWO: mint XRP NFT
            return render(request, "generate.html", {'data' : data})
    else:
        form = UploadFileForm()
        context = {
            'form':form,
        }
    
    #return render(request, 'books_website/UploadBook.html', context)

    return render(request, "create.html", context)

def write_metadata(file):
    data = file    
# STEP TWO: wrap that up in the details template

    collectible_metadata = sample_metadata.metadata_template

    filepath = file.file.url
    #cleaned_title = filepath.split("/")[-1].split("_")[0] + "." + filepath.split("/")[-1].split(".")[-1]
    cleaned_title = filepath.split("/")[-1].split(".")[0].split("_")[0]
    metadata_filename = (
        "./metadata/testnet/" + cleaned_title + ".json"
    )

    if Path(metadata_filename).exists():
        logging.info("metadata file {} already exists ".format(metadata_filename))
    else:
        logging.info("create metadata file {} ".format(metadata_filename))
        collectible_metadata["title"] = file.title
        collectible_metadata["description"] = file.description
        logging.info(collectible_metadata)

        img_uri = None
        # Upload image to IPFS and return the URI
        img_uri = upload_to_ipfs("." + filepath)
        collectible_metadata["image"] = img_uri
        data.ipfs_uri = img_uri
        logging.info(collectible_metadata)

        # Write to metada file
        with open(metadata_filename, "w") as file:
            json.dump(collectible_metadata, file)
            
        metadata_uri = upload_to_ipfs(metadata_filename)
        collectible_metadata["metadata"] = metadata_uri
        
        # TODO: find a better way to overwrite
        with open(metadata_filename, "w") as file:
            json.dump(collectible_metadata, file)
            

    with open(metadata_filename) as f:
        collectible_metadata = json.load(f)
        data.ipfs_uri = collectible_metadata["image"]
        data.metadata_uri = collectible_metadata["metadata"]
        data.collectible_metadata = collectible_metadata
        
    return data
    

def upload_to_ipfs(filePath):
    
    if os.getenv("UPLOAD_IPFS") != "true":
        logging.error("Not uploading to IPFS because env variable is disabled")
        return None
    else:
        logging.info("UPLOAD_IPFS is set to true, uploading now")


    # abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filePath)
    logging.info("Retrieving file at: " + filePath) # type is `str`

    # TODO: don't upload if it's already there
    
    with Path(filePath).open("rb") as fp:
        img_binary = fp.read()
        response = requests.post(ipfs_url + '/api/v0/add', files={"file": img_binary})
        logging.info(response.json())
        ipfs_hash = response.json()["Hash"]
        filename = filePath.split("/")[-1:][0]
        logging.info("ipfs_hash "+ ipfs_hash)
        logging.info("filename "+ filename)
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        return uri
    
    # return None
        
