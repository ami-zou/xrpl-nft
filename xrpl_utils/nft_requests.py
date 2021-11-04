import xrpl
import xrpl_py
import json
from pathlib import Path

TESTNET_URL = "https://s.altnet.rippletest.net:51234"

ISSUER_ADDR = "rHBdNmoeV4pD1oXCFrAf1VF4bjK7jSfCEK"
ISSUER_SEED = "sEdTXHMFuhLAP6cL47MhtvEA3F3Ptnc"
ISSUER_SEQUENCE = 22401993

DISTRIBUTER_ADDR = "rJwEwKCjxVcGCbb6a4z8obEsGQxMUj2VFg"
DISTRIBUTER_SEED = "sEd7wZAr6nRhCP4xVjDumW6CMpWwTmy"
DISTRIBUTER_SEQUENCE = 22400988

NFT_QUANTITY = "1000000000000000e-96"

client = xrpl.clients.JsonRpcClient(TESTNET_URL)

issuer_wallet = xrpl_py.get_wallet(ISSUER_SEED, ISSUER_SEQUENCE)
print(" Issuer wallet public key", issuer_wallet.public_key)

distributer_wallet = xrpl_py.get_wallet(DISTRIBUTER_SEED, DISTRIBUTER_SEQUENCE)
print(" Distributer wallet public key", distributer_wallet.public_key)

# with Path("./data/1-accountset.json").open("rb") as file:
#     input = json.load(file)
#     print(type(input))
#     print(input)

    # tx_accountset = xrpl.models.base_model.BaseModel.from_dict(input)

# STEP ONE: AccountSet
META_HEX = "68747470733a2f2f697066732e696f2f697066732f516d556a34664d31726f39674131564e5a776150714235377a67555262526a517753396e6b4132684278714c58443f66696c656e616d653d7872702e6a736f6e"
# tx_accountset = xrpl_py.prepare_accountset(ISSUER_ADDR, META_HEX)

# tx_accountset_link = xrpl_py.tx_lifecycle(tx_accountset, issuer_wallet, client)
# print("AccountSet TX explorer: ", tx_accountset_link)

# STEP TWO: TrustSet
FILE_HASH_SHA = "FD5FCE11F002FEA1DCC4C8AA492A1AE68590B4D5"
currency_code = FILE_HASH_SHA

tx_trustset = xrpl_py.prepare_trustset(DISTRIBUTER_ADDR, currency_code, ISSUER_ADDR)
tx_trustset_link = xrpl_py.tx_lifecycle(tx_trustset, distributer_wallet, client)
print("TrustSet TX explorer: ", tx_trustset_link)

# STEP THREE: Issue token
# tx_issue_token = xrpl_py.prepare_issue_token(DISTRIBUTER_ADDR, currency_code, ISSUER_ADDR)
# tx_issue_token_link = xrpl_py.tx_lifecycle(tx_issue_token, issuer_wallet, client)
# print("Issue Token TX explorer: ", tx_issue_token_link)