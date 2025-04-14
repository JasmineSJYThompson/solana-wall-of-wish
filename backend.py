from fastapi import FastAPI, HTTPException
from solana.rpc.api import Client
from solana.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey
from solana.transaction import Transaction, TransactionInstruction
from solana.system_program import SYS_PROGRAM_ID
import base58
import struct
import time
import os
import streamlit as st
import json

app = FastAPI()

# Constants
DEVNET_URL = "https://api.devnet.solana.com"
# This is a placeholder program ID - you'll need to replace it with your actual program ID
PROGRAM_ID = PublicKey("YOUR_PROGRAM_ID")

# Initialize Solana client
solana_client = Client(DEVNET_URL)

# Get private key from Streamlit secrets
try:
    PRIVATE_KEY = st.secrets["PRIVATE_KEY"]
    keypair = Keypair.from_secret_key(base58.b58decode(PRIVATE_KEY))
except Exception as e:
    print(f"Error loading private key: {e}")
    keypair = None

@app.post("/submit_wish")
async def submit_wish(request: dict):
    if not keypair:
        raise HTTPException(status_code=500, detail="Private key not configured")
    
    try:
        # Get title and public key from request
        title = request.get("title")
        public_key_str = request.get("public_key")
        
        if not title or not public_key_str:
            raise HTTPException(status_code=400, detail="Missing title or public key")
        
        # Validate the public key
        user_public_key = PublicKey(public_key_str)
        
        # Generate PDA for the wish
        # PDAs are special addresses that can only be created by the program
        # We use the user's public key and timestamp to create a unique PDA for each wish
        wish_seed = f"wish_{user_public_key}_{int(time.time())}"
        [wish_pda, _] = PublicKey.find_program_address(
            [bytes(wish_seed, "utf-8")],
            PROGRAM_ID
        )
        
        # Create instruction data
        # This is the data that will be stored on-chain
        instruction_data = bytes([0])  # Instruction discriminator
        instruction_data += struct.pack("<I", len(title))  # String length
        instruction_data += title.encode()  # Title string
        
        # Create instruction
        instruction = TransactionInstruction(
            keys=[
                {"pubkey": wish_pda, "is_signer": False, "is_writable": True},  # PDA account to store the wish
                {"pubkey": user_public_key, "is_signer": True, "is_writable": True},  # User's account
                {"pubkey": SYS_PROGRAM_ID, "is_signer": False, "is_writable": False}  # System program
            ],
            program_id=PROGRAM_ID,
            data=instruction_data
        )
        
        # Create and send transaction
        transaction = Transaction()
        transaction.add(instruction)
        
        result = solana_client.send_transaction(transaction, keypair)
        return {"success": True, "signature": result["result"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_wishes")
async def get_wishes():
    try:
        # Get all program accounts
        accounts = solana_client.get_program_accounts(PROGRAM_ID)
        wishes = []
        
        for account in accounts["result"]:
            data = account["account"]["data"]
            author = PublicKey(data[8:40])
            timestamp = struct.unpack("<q", data[40:48])[0]
            title_length = struct.unpack("<I", data[48:52])[0]
            title = data[52:52+title_length].decode()
            
            wishes.append({
                "title": title,
                "author": str(author),
                "timestamp": timestamp
            })
        
        return sorted(wishes, key=lambda x: x["timestamp"], reverse=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 