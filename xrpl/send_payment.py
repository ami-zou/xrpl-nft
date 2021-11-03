
# Example Credentials ----------------------------------------------------------
from xrpl.wallet import Wallet
test_wallet = Wallet(seed="sEdTxeHLBggLL7SoQdZryqywvXfByjq", sequence=22400937)
print("\nSender Classic address:", test_wallet.classic_address) # raMVC6xHMv2mjGHmWAdcZy12WJknTqHVTg

# Connect ----------------------------------------------------------------------
import xrpl
testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

# Prepare payment
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops


my_tx_payment = Payment(
    account=test_wallet.classic_address,
    amount=xrp_to_drops(22),
    destination="rJwEwKCjxVcGCbb6a4z8obEsGQxMUj2VFg",
)
print("\nPayment object:", my_tx_payment)

# Prepare transaction ----------------------------------------------------------
my_payment = xrpl.models.transactions.Payment(
    account=test_wallet.classic_address,
    amount=xrpl.utils.xrp_to_drops(22),
    destination="rJwEwKCjxVcGCbb6a4z8obEsGQxMUj2VFg",
)
print("\nPayment object:", my_payment)

# Sign transaction -------------------------------------------------------------

# Sign the transaction
from xrpl.transaction import safe_sign_and_autofill_transaction

my_tx_payment_signed = safe_sign_and_autofill_transaction(my_tx_payment,test_wallet, client)

signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
        my_payment, test_wallet, client)
max_ledger = signed_tx.last_ledger_sequence
tx_id = signed_tx.get_hash()
print("\nSigned transaction:", signed_tx)
print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_tx.fee), "XRP")
print("Transaction expires after ledger:", max_ledger)
print("Identifying hash:", tx_id)

print("\nSigned transaction:", my_tx_payment_signed)



# Submit and send the transaction
from xrpl.transaction import send_reliable_submission

tx_response = send_reliable_submission(my_tx_payment_signed, client)

# Submit transaction -----------------------------------------------------------
try:
    tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
except xrpl.transaction.XRPLReliableSubmissionException as e:
    exit(f"Submit failed: {e}")

## NOTICE: the above might take 4-7 sec

# Check transaction results ----------------------------------------------------
import json
print(json.dumps(tx_response.result, indent=4, sort_keys=True))
print(f"Explorer link: https://testnet.xrpl.org/transactions/{tx_id}")
metadata = tx_response.result.get("meta", {})
print(metadata)
if metadata.get("TransactionResult"):
    print("Result code:", metadata["TransactionResult"])
if metadata.get("delivered_amount"):
    print("XRP delivered:", xrpl.utils.drops_to_xrp(
                metadata["delivered_amount"]))