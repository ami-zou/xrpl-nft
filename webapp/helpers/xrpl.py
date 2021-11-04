import logging
from .utils import to_sha1
from .utils import memo_to_hex
from .utils import get_explorer_addr
logging.basicConfig(level=logging.INFO)
import xrpl
from xrpl.wallet import generate_faucet_wallet

NFT_QUANTITY = "1000000000000000e-96"

def mint_nft(data):
    title = data.title
    metadata_uri = data.metadata_uri
    logging.info("Minting NFT for title {} and metadata_uri {}".format(title, metadata_uri))

    FILE_URL = data.file_uri #"https://ipfs.io/ipfs/QmPV1x4oxx977wPRBXWMXDsv8DF9RXauxVhEnjGrkWGhPQ?filename=xrp.png"
    FILE_HASH = data.file_hash #"QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD"
    META_URL = data.metadata_uri #"https://ipfs.io/ipfs/QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD?filename=xrp.json"

    # Compute the variables ----
    FILE_HASH_SHA = to_sha1(FILE_HASH)
    MEMO_DATA_HEX = memo_to_hex(FILE_URL, META_URL)

    issuer_addr = "Not set"
    issuer_explorer ="Not set"
    distributor_addr = "Not set"
    distributor_explorer = "Not set"
    issued_token_link = "Not set"

    # Connect ----------------------------------------------------------------------
    testnet_url = "https://s.altnet.rippletest.net:51234"
    client = xrpl.clients.JsonRpcClient(testnet_url)


    # STEP ONE: Get credentials from the Testnet Faucet --------------------------------------
    # For production, instead create a Wallet instance
    faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    print("\nGetting new issuer and distributer accounts from the Testnet faucet...")
    cold_wallet = generate_faucet_wallet(client, debug=True)
    issuer_addr = cold_wallet.classic_address
    issuer_explorer = get_explorer_addr(issuer_addr)
    print(f"Issuer wallet classic address {cold_wallet.classic_address}, seed {cold_wallet.seed}, and sequence {cold_wallet.sequence}")
    hot_wallet = generate_faucet_wallet(client, debug=True)
    distributor_addr = hot_wallet.classic_address
    distributor_explorer = get_explorer_addr(distributor_addr)
    print(f"Distributer wallet classic address {hot_wallet.classic_address}, seed {hot_wallet.seed}, and sequence {hot_wallet.sequence}")


    # Configure issuer (cold address) settings -------------------------------------
    cold_settings_tx = xrpl.models.transactions.AccountSet(
        account=cold_wallet.classic_address,
        transfer_rate=0,
        tick_size=5,
        domain=bytes.hex(META_URL.encode("ASCII")),
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE, #OR set it to 8
    )
    cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=cold_settings_tx,
        wallet=cold_wallet,
        client=client,
    )
    print("\nSending issuer address AccountSet transaction...")
    response = xrpl.transaction.send_reliable_submission(cst_prepared, client)
    print(response)


    # Configure hot address settings -----------------------------------------------
    hot_settings_tx = xrpl.models.transactions.AccountSet(
        account=hot_wallet.classic_address,
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
    )
    hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=hot_settings_tx,
        wallet=hot_wallet,
        client=client,
    )
    print("\nSending distributor address AccountSet transaction...")
    response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
    print(response)


    # STEP TWO: Create trust line from hot to cold address -----------------------------------
    currency_code = FILE_HASH_SHA #"fd5fce11f002fea1dcc4c8aa492a1ae68590b4d5".upper()
    trust_set_tx = xrpl.models.transactions.TrustSet(
        account=hot_wallet.classic_address,
        limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=NFT_QUANTITY, # Large limit, arbitrarily chosen -- 10000000000
        )
    )
    ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=trust_set_tx,
        wallet=hot_wallet,
        client=client,
    )
    print("\nCreating trust line from distributer address to issuer...")
    response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
    print(response)


    # STEP THREE: Issue token -------------------------------------------------------------------
    issue_quantity = NFT_QUANTITY
    print(f"\nPrepare token {FILE_HASH_SHA}...")
    send_token_tx = xrpl.models.transactions.Payment(
        account=cold_wallet.classic_address,
        destination=hot_wallet.classic_address,
        amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=issue_quantity
        ),
        memos=[xrpl.models.transactions.Memo(
            #memo_type = MEMO_TYPE_HEX,
            memo_data = MEMO_DATA_HEX
        )]
    )
    pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=send_token_tx,
        wallet=cold_wallet,
        client=client,
    )
    print(f"\nSending {issue_quantity} NFT: {currency_code} to {hot_wallet.classic_address}...")
    response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
    print(response)

    tx_id = pay_prepared.get_hash()
    issued_token_link =f"https://testnet.xrpl.org/transactions/{tx_id}"
    print("\n issue token transaction details: ", issued_token_link)


    # Check balances ---------------------------------------------------------------
    print("\nGetting distributer address balances...")
    response = client.request(xrpl.models.requests.AccountLines(
        account=hot_wallet.classic_address,
        ledger_index="validated",
    ))
    print(response)

    print("\nGetting issuer address balances...")
    response = client.request(xrpl.models.requests.GatewayBalances(
        account=cold_wallet.classic_address,
        ledger_index="validated",
        hotwallet=[hot_wallet.classic_address]
    ))
    print(response)

    data.issuer_addr = issuer_addr
    data.issuer_explorer = issuer_explorer
    data.distributor_addr = distributor_addr
    data.distributor_explorer = distributor_explorer
    data.issued_token_link = issued_token_link

    return data