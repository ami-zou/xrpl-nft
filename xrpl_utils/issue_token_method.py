import utils
import logging
import xrpl
from xrpl.wallet import generate_faucet_wallet
logging.basicConfig(level=logging.INFO)

NFT_QUANTITY = "1000000000000000e-96"

def issue_nft(data):
    title = data.title
    metadata_uri = data.metadata_uri
    logging.info("Minting NFT for title {} and metadata_uri {}".format(title, metadata_uri))

    FILE_URL = data.file_uri #"https://ipfs.io/ipfs/QmPV1x4oxx977wPRBXWMXDsv8DF9RXauxVhEnjGrkWGhPQ?filename=xrp.png"
    FILE_HASH = data.file_hash #"QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD"
    META_URL = data.metadata_uri #"https://ipfs.io/ipfs/QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD?filename=xrp.json"

    # Compute the variables ----
    
    FILE_HASH_SHA = utils.to_sha1(FILE_HASH)
    #META_HEX = "68747470733a2f2f697066732e696f2f697066732f516d556a34664d31726f39674131564e5a776150714235377a67555262526a517753396e6b4132684278714c58443f66696c656e616d653d7872702e6a736f6e"
    #MEMO_DATA_HEX = "7B0A202020202246696C65223A202268747470733A2F2F697066732E696F2F697066732F516D50563178346F78783937377750524258574D584473763844463952586175785668456E6A47726B57476850513F66696C656E616D653D7872702E706E67222C0A20202020224D65746164617461223A202268747470733A2F2F697066732E696F2F697066732F516D556A34664D31726F39674131564E5A776150714235377A67555262526A517753396E6B4132684278714C58443F66696C656E616D653D7872702E6A736F6E220A7D"
    MEMO_DATA_HEX = utils.memo_to_hex(FILE_URL, META_URL)
    #MEMO_TYPE_HEX = bytes.hex("NFT Details".encode("ASCII")).upper()

    issuer_addr = ""
    issuer_explorer =""
    distributor_addr = ""
    distributor_explorer = ""
    issued_token_link = ""

    # Connect ----------------------------------------------------------------------
    
    testnet_url = "https://s.altnet.rippletest.net:51234"
    client = xrpl.clients.JsonRpcClient(testnet_url)

    # STEP ONE: Get credentials from the Testnet Faucet --------------------------------------
    # For production, instead create a Wallet instance
    faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    print("\nGetting 2 new accounts from the Testnet faucet...")
    cold_wallet = generate_faucet_wallet(client, debug=True)
    issuer_addr = cold_wallet.classic_address
    issuer_explorer = utils.get_explorer_addr(issuer_addr)
    print(f"cold/issuer wallet classic address {cold_wallet.classic_address}, seed {cold_wallet.seed}, and sequence {cold_wallet.sequence}")
    hot_wallet = generate_faucet_wallet(client, debug=True)
    distributor_addr = hot_wallet.classic_address
    distributor_explorer = utils.get_explorer_addr(distributor_addr)
    print(f"hot/distributer wallet classic address {hot_wallet.classic_address}, seed {hot_wallet.seed}, and sequence {hot_wallet.sequence}")


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
    print("\nSending issuer/cold address AccountSet transaction...")
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
    print("\nSending distributer/hot address AccountSet transaction...")
    response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
    print(response)


    # STEP TWO: Create trust line from hot to cold address -----------------------------------
    # currency_code = "FOO"
    # currency_code = "QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD"
    # currency_code = "fd5fce11f002fea1dcc4c8aa492a1ae68590b4d5"
    # currency_code = "0158415500000000C1F76FF6ECB0BAC600000000"
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
    print("\nCreating trust line from hot/distributer address to issuer...")
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
    print("\nGetting hot/distributer address balances...")
    response = client.request(xrpl.models.requests.AccountLines(
        account=hot_wallet.classic_address,
        ledger_index="validated",
    ))
    print(response)

    print("\nGetting cold/sender address balances...")
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