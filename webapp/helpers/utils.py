from pathlib import Path
import json
import codecs
import hashlib


def to_sha1(input):
    h = hashlib.sha1(input.encode('utf-8'))
    output = h.hexdigest().upper()
    print("\n SHA1 value: ",output)
    print("output length ", len(output))
    return output

def to_hex(input_string):
    print("\n input data:", input_string)
    output_hex = input_string.encode('utf-8').hex().upper()
    print("\n HEX output data:", output_hex)
    return output_hex


def file_to_hex(filename):
    with Path(filename).open("rb") as file:
        input = json.load(file)
        # print(type(input))
        
        text = json.dumps(input, sort_keys=True,
        indent=4, separators=(',', ': '))
        # print(type(text))

        hex_value = to_hex(text)
        return hex_value

def memo_to_hex(file_url, meta_url):
    data = {
        'file_url' : file_url,
        'metadata_url' :  meta_url
    }

    return to_hex(str(data))


def hex_to_ascii(hex_string):
    binary_str = codecs.decode(hex_string, "hex")
    string_value = str(binary_str,'utf-8')
    print(string_value)
    return string_value
    
def get_explorer_addr(account):
    return f"https://test.bithomp.com/explorer/{account}"


# -----------TESTING---------------------------------------
# hex_string = to_hex("https://ipfs.io/ipfs/QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD?filename=xrp.json")
# hex_to_ascii(hex_string)

# file_hex_string = file_to_hex("./data/0-memo.json")
# hex_to_ascii(file_hex_string)

# hash_input = "QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD"
# print(hash_input)
# to_sha1(hash_input)

# file_url = "https://ipfs.io/ipfs/QmPV1x4oxx977wPRBXWMXDsv8DF9RXauxVhEnjGrkWGhPQ?filename=xrp.png"
# meta_url = "https://ipfs.io/ipfs/QmUj4fM1ro9gA1VNZwaPqB57zgURbRjQwS9nkA2hBxqLXD?filename=xrp.json"
# memo_to_hex(file_url, meta_url)