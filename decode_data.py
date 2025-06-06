import requests
import json

url = "https://api.devnet.solana.com"

pda = "AXG5yPrycHiZ5hzEGebRjge6HsdGArpkL7uyrwok6vnJ"

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getAccountInfo",
    "params": [pda]
}

response = requests.post(url, json=payload)
response_json = response.json()

import base58
from struct import unpack

#b58_data = "EJLbdAgd22fDcpovK3woGAJTv5q3xDPvyiWspiynDRSz78wVp2C42cPooLhC6T1QkLvmdSLBK1xEZcBBEqsDd8QaK715h"
b58_data = response_json["result"]["value"]["data"]

raw = base58.b58decode(b58_data)

# Skip 8-byte discriminator
data = raw[8:]

# Extract fields
user_pubkey_bytes = data[:32]
wish_len = unpack("<I", data[32:36])[0]
wish = data[36:36 + wish_len].decode("utf-8")
bump = data[36 + wish_len]

print("User pubkey:", base58.b58encode(user_pubkey_bytes).decode())
print("Wish:", wish)
print("Bump:", bump)
