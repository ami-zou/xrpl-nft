import xrpl
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.models.transactions import AccountSet
from xrpl.models.transactions import TrustSet
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.currencies import Currency
from xrpl.utils import xrp_to_drops
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.transaction import send_reliable_submission
import json

NFT_QUANTITY = "1000000000000000e-96"
TESTNET_URL = "https://s.altnet.rippletest.net:51234"

def get_wallet(seed, sequence): # sEdTxeHLBggLL7SoQdZryqywvXfByjq, 22400937
    wallet = Wallet(seed=seed, sequence=sequence) 
    print("\nWallet classic address:", wallet.classic_address) # raMVC6xHMv2mjGHmWAdcZy12WJknTqHVTg
    return wallet

def prepare_payment(sender_account, destination_account, amount):
    tx_payment = Payment(
        account=sender_account,
        amount=xrp_to_drops(22), #TODO: make the amount a variable -- need to check type
        destination=destination_account,
    )
    print("\nPayment object:\n", tx_payment)
    return tx_payment

def prepare_accountset(account, domain, flag=8):
    tx_accountset = AccountSet(
        account = account,
        domain = domain,
        set_flag = flag
    )
    # domain=bytes.hex("example.com".encode("ASCII"))
    return tx_accountset

def prepare_trustset(distributer_address, currency_code, issuer_address):
    trust_set_tx = xrpl.models.transactions.TrustSet(
        account=distributer_address,
        limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=issuer_address,
            value=NFT_QUANTITY, # Large limit, arbitrarily chosen
        )
    )
    print("\ntrust_set_tx: " , trust_set_tx)
    return trust_set_tx

def prepare_issue_token(distributer_addr, currency_code, issuer_addr):
    send_token_tx = xrpl.models.transactions.Payment(
        account=issuer_addr,
        destination=distributer_addr,
        amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=issuer_addr,
            value=NFT_QUANTITY
        )
    )
    print("\nissue token: ", send_token_tx)
    return send_token_tx


def sign_transaction(tx, wallet, client):
    signed_tx = safe_sign_and_autofill_transaction(tx, wallet, client)
    max_ledger = signed_tx.last_ledger_sequence
    tx_id = signed_tx.get_hash()
    print("\nSigned transaction:\n", signed_tx)
    print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_tx.fee), "XRP")
    print("Transaction expires after ledger:", max_ledger)
    print("Identifying hash:", tx_id)
    return signed_tx

def submit_transaction(signed_tx, client):
    try:
        tx_response = send_reliable_submission(signed_tx, client)
        return tx_response
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        exit(f"Submit failed: {e}")

def transaction_status(tx_response, tx_id):
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    print(f"\nExplorer link: https://testnet.xrpl.org/transactions/{tx_id}")
    metadata = tx_response.result.get("meta", {})
    print(metadata)
    if metadata.get("TransactionResult"):
        print("\n Result code:", metadata["TransactionResult"])
    if metadata.get("delivered_amount"):
        print("\n XRP delivered:", xrpl.utils.drops_to_xrp(
                    metadata["delivered_amount"]))

def tx_lifecycle(tx, wallet, client):

    print("\nIntended TX: \n", tx)
    
    signed_tx = sign_transaction(tx, wallet, client)
    tx_id = signed_tx.get_hash()
    print("\nTX ID hash: ", tx_id)

    tx_response = submit_transaction(signed_tx, client)
    print("\nSubmitted TX:\n", tx_response)
    
    transaction_status(tx_response, tx_id)

    explorer_link = f"https://testnet.xrpl.org/transactions/{tx_id}"
    return explorer_link


# --- NOT USED BUT MIGHT BE HELPFUL ---
def prepare_currency(currency, issuer):
    prepared_currency = Currency (
        currency = currency,
        issuer = issuer,
    )
    print("\ncurrency to be issued:\n", prepared_currency)
    return prepared_currency

def nft_limit_amount(currency):
    limit_amount = IssuedCurrencyAmount (
        currency = currency["currency"],
        issuer = currency["issuer"],
        value = NFT_QUANTITY
    )
    print("\n limit amount is: ", limit_amount)
    return limit_amount