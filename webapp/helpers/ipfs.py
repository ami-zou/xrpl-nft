import logging
import requests
from pathlib import Path
import os
from metadata import sample_metadata
from media import *
import json

logging.basicConfig(level=logging.INFO)
ipfs_url = "http://localhost:5001"

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
        img_hash = None
        # Upload image to IPFS and return the URI
        # TODO: might throw an error here when UPLOAD_IPS is disabled
        img_hash, img_uri = upload_to_ipfs("." + filepath)
        collectible_metadata["file_hash"] = img_hash
        collectible_metadata["file_uri"] = img_uri
        #data.file_uri = img_uri
        logging.info(collectible_metadata)

        # Write to metada file
        with open(metadata_filename, "w") as file:
            json.dump(collectible_metadata, file)
            
        meta_hash = None
        metadata_uri = None
        meta_hash, metadata_uri = upload_to_ipfs(metadata_filename)
        collectible_metadata["metadata_uri"] = metadata_uri
        collectible_metadata["metadata_hash"] = meta_hash
        
        # TODO: find a better way to overwrite
        with open(metadata_filename, "w") as file:
            json.dump(collectible_metadata, file)
            

    with open(metadata_filename) as f:
        collectible_metadata = json.load(f)
        data.file_uri = collectible_metadata["file_uri"]
        data.file_hash = collectible_metadata["file_hash"]
        data.metadata_uri = collectible_metadata["metadata_uri"]
        data.metadata_hash = collectible_metadata["metadata_hash"]
        # print(type(collectible_metadata))
        data_str = json.dumps(collectible_metadata)
        # print(type(data_str))
        data.collectible_metadata = data_str
        # print(data.collectible_metadata)
        
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
        logging.info(uri)
        return ipfs_hash, uri
    
    # return None