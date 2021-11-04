# XRP NFT

## Upload a file and related metadata directly to IPFS
* run an IPFS node locally
* front-end to upload the file
* then upload the file directly to IPFS to obtain a file hash
* embed that file hash or url into the metadata json file, and then upload the json file to IPFS as well, and obtain the metadata hash or url

## Auto-generate issuer and distributor accounts/wallets on XRP Testnet
* using `xrpl-py` to generate issuer and distributor accounts
* issuer's domain points to the IPFS metadata link
* establish trustline between issuer and distribotor

## Issue an NFT on XRPL
* following proposal in XLS-14d (https://github.com/XRPLF/XRPL-Standards/discussions/30)
* issue a token with `currency_code = {HEX value of the IPFS metadata hash}`
* token has the minimum amount of XRP drop (`"1000000000000000e-96"`)
* in `Memo` field, it contains info for the two IPFS pointers
  * one for the actual file
  * and the other for the metadata
  
  
