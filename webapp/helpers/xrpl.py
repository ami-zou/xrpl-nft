import logging

logging.basicConfig(level=logging.INFO)


def mint_nft(data):
    title = data.title
    metadata_uri = data.metadata_uri
    logging.info("Minting NFT for title {} and metadata_uri {}".format(title, metadata_uri))


    return data