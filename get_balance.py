import requests
import json

# Solana Devnet endpoint
url = "https://api.devnet.solana.com"

# Example: Get the balance of a public key
public_key = "FQfk317MxfMfHZq46xZACgg5em9xd5KUZRyFwJBVLQqy"  # Replace with your public key

# Prepare the JSON-RPC payload
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBalance",
    "params": [public_key],
}

# Send the request
response = requests.post(url, json=payload)

# Parse and print the response
response_json = response.json()

if "result" in response_json:
    print(f"Balance for {public_key}: {response_json['result']['value']} lamports")
else:
    print("Error:", response_json.get("error", "Unknown error"))
