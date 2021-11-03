import xrpl
import xrpl_py


TESTNET_URL = "https://s.altnet.rippletest.net:51234"

PUBLIC_ADDRESS_1 = "raMVC6xHMv2mjGHmWAdcZy12WJknTqHVTg"
SEED_1 = "sEdTxeHLBggLL7SoQdZryqywvXfByjq"
SEQUENCE_1 = 22400937

PUBLIC_ADDRESS_2 = "rJwEwKCjxVcGCbb6a4z8obEsGQxMUj2VFg"
SEED_2 = "sEd7wZAr6nRhCP4xVjDumW6CMpWwTmy"
SEQUENCE_2 = 22400988

client = xrpl.clients.JsonRpcClient(TESTNET_URL)

wallet = xrpl_py.get_wallet(SEED_1, SEQUENCE_1)
print(" Wallet public key", wallet.public_key)

# ----------- Send a Payment -------------------------
payment = xrpl_py.prepare_payment(PUBLIC_ADDRESS_1, PUBLIC_ADDRESS_2, 8)

# signed_tx = xrpl_py.sign_transaction(payment, wallet, client)
# tx_id = signed_tx.get_hash()

# tx_response = xrpl_py.submit_transaction(signed_tx, client)
# print("\nSubmitted tx:\n", tx_response)

# xrpl_py.payment_status(tx_response, tx_id)

link = xrpl_py.tx_lifecycle(payment, wallet, client)
print("returned link: ", link)