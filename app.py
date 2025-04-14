import streamlit as st
from solana.rpc.api import Client
from solana.publickey import PublicKey
import asyncio
import time
import requests

# Constants
DEVNET_URL = "https://api.devnet.solana.com"
PROGRAM_ID = "YOUR_PROGRAM_ID"  # Replace with your deployed program ID
BACKEND_URL = "http://localhost:8000"  # Change this to your deployed backend URL

# Initialize Solana client
solana_client = Client(DEVNET_URL)

def main():
    st.title("Solana Wall of Wish")
    st.write("A decentralized wish wall built on Solana blockchain")
    st.write("Connected to: Devnet")
    
    # Sidebar for wallet connection
    with st.sidebar:
        st.header("Wallet Connection")
        
        # Try to get stored public key
        stored_public_key = None
        try:
            stored_public_key = st.secrets["PUBLIC_KEY"]
            st.write("Stored Public Key:", stored_public_key[:8] + "..." + stored_public_key[-8:])
        except:
            st.info("No stored public key found")
        
        # Option to use stored key or input new one
        use_stored_key = False
        if stored_public_key:
            use_stored_key = st.checkbox("Use stored public key", value=True)
        
        if not use_stored_key:
            user_public_key = st.text_input("Enter your Solana public key")
            if user_public_key:
                try:
                    # Validate the public key
                    PublicKey(user_public_key)
                    st.success("Valid public key!")
                    public_key = user_public_key
                except:
                    st.error("Invalid public key format")
                    public_key = None
            else:
                public_key = None
        else:
            public_key = stored_public_key
        
        if public_key:
            st.success(f"Connected to wallet: {public_key[:8]}...{public_key[-8:]}")
    
    # Main content
    st.header("Make a Wish")
    wish_text = st.text_area("Write your wish here")
    
    if st.button("Submit Wish"):
        if wish_text and public_key:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/submit_wish",
                    json={
                        "title": wish_text,
                        "public_key": public_key
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Wish submitted successfully!")
                    st.write(f"Transaction signature: {result['signature']}")
                else:
                    st.error(f"Error submitting wish: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please connect your wallet and write a wish first")
    
    # Display existing wishes section
    st.header("Recent Wishes")
    try:
        response = requests.get(f"{BACKEND_URL}/get_wishes")
        if response.status_code == 200:
            wishes = response.json()
            if wishes:
                for wish in wishes:
                    with st.expander(f"Wish by {wish['author'][:8]}..."):
                        st.write(f"Title: {wish['title']}")
                        st.write(f"Time: {time.ctime(wish['timestamp'])}")
            else:
                st.info("No wishes found. Be the first to make a wish!")
        else:
            st.error("Error fetching wishes")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 