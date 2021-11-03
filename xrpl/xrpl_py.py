import xrpl
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.transaction import send_reliable_submission
import json



TESTNET_URL = "https://s.altnet.rippletest.net:51234"

def get_wallet(seed, sequence): # sEdTxeHLBggLL7SoQdZryqywvXfByjq, 22400937
    wallet = Wallet(seed=seed, sequence=sequence) 
    print("\nWallet classic address:", wallet.classic_address) # raMVC6xHMv2mjGHmWAdcZy12WJknTqHVTg
    return wallet

def prepare_payment(sender_account, destination_account, amount):
    my_tx_payment = Payment(
        account=sender_account,
        amount=xrp_to_drops(22), #TODO: make the amount a variable -- need to check type
        destination=destination_account,
    )
    print("\nPayment object:\n", my_tx_payment)
    return my_tx_payment

def sign_transaction(payment, wallet, client):
    signed_tx = safe_sign_and_autofill_transaction(payment, wallet, client)
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

def payment_status(tx_response, tx_id):
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    print(f"\nExplorer link: https://testnet.xrpl.org/transactions/{tx_id}")
    metadata = tx_response.result.get("meta", {})
    print(metadata)
    if metadata.get("TransactionResult"):
        print("\n Result code:", metadata["TransactionResult"])
    if metadata.get("delivered_amount"):
        print("\n XRP delivered:", xrpl.utils.drops_to_xrp(
                    metadata["delivered_amount"]))