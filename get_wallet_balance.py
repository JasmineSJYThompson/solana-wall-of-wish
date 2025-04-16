import streamlit as st
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Connect to Solana devnet (or mainnet if you want to use that)
client = Client("https://api.devnet.solana.com")

st.title("🎉 Wish Board")

# Fetch recent transactions for a given program
# You'd typically query the program's transactions here
def get_recent_transactions(pubkey: str):
    pubkey = Pubkey.from_string(pubkey)
    # Assuming the wish program signature is here
    # Example: query all recent signatures for this public key
    response = client.get_signatures_for_address(pubkey)
    return response.value

# Sample public key (Replace with your program address or the address of a user who submits wishes)
program_pubkey = st.text_input("Enter Program Public Key:", "FQfk317MxfMfHZq46xZACgg5em9xd5KUZRyFwJBVLQqy")
if program_pubkey:
    transactions = get_recent_transactions(program_pubkey)
    if transactions:
        st.write("Recent Transactions:")

        # Show transaction results
        for txn in transactions:
            tx_hash = txn.signature
            # Here you can add logic to fetch the actual wish details if they are stored in a transaction (simplified)
            st.write(f"Transaction {tx_hash}")

            try:
                logs = txn.message
                st.write(logs)
                if logs:
                    st.text("Transaction logs:")
                    for log in logs:
                        st.text(log)
            except:
                pass
    else:
        st.write("No transactions found for this address.")
