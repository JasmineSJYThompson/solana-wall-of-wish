import streamlit as st
import requests
import json
from seahorse.prelude import *
from seahorse.keypair import Keypair
from seahorse.publickey import PublicKey
import time

# Constants
BACKEND_URL = "http://localhost:8000"
WALLET_CONNECTED = False

def connect_wallet():
    """Connect to a Solana wallet using Seahorse"""
    try:
        # In a real app, this would connect to a wallet like Phantom
        # For demo purposes, we'll simulate a wallet connection
        st.session_state.wallet_connected = True
        st.session_state.public_key = "YourPublicKeyHere"  # Replace with actual public key
        return True
    except Exception as e:
        st.error(f"Failed to connect wallet: {str(e)}")
        return False

def submit_wish(title):
    """Submit a wish to the blockchain"""
    if not st.session_state.get('wallet_connected'):
        st.error("Please connect your wallet first")
        return
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/submit_wish",
            json={
                "title": title,
                "public_key": st.session_state.public_key
            }
        )
        
        if response.status_code == 200:
            st.success("Wish submitted successfully!")
            st.balloons()
        else:
            st.error(f"Failed to submit wish: {response.text}")
    
    except Exception as e:
        st.error(f"Error submitting wish: {str(e)}")

def display_wishes():
    """Display all wishes from the blockchain"""
    try:
        response = requests.get(f"{BACKEND_URL}/get_wishes")
        
        if response.status_code == 200:
            wishes = response.json()
            
            for wish in wishes:
                with st.expander(f"Wish by {wish['author'][:8]}... at {time.ctime(wish['timestamp'])}"):
                    st.write(wish['title'])
        else:
            st.error(f"Failed to fetch wishes: {response.text}")
    
    except Exception as e:
        st.error(f"Error fetching wishes: {str(e)}")

def main():
    st.title("🎋 Solana Wall of Wishes")
    st.write("Share your wishes on the Solana blockchain!")
    
    # Wallet connection
    if not st.session_state.get('wallet_connected'):
        if st.button("Connect Wallet"):
            if connect_wallet():
                st.success("Wallet connected successfully!")
    
    # Wish submission
    if st.session_state.get('wallet_connected'):
        st.subheader("Make a Wish")
        wish_title = st.text_input("Enter your wish:")
        
        if st.button("Submit Wish"):
            if wish_title:
                submit_wish(wish_title)
            else:
                st.warning("Please enter a wish first")
    
    # Display wishes
    st.subheader("Recent Wishes")
    display_wishes()

if __name__ == "__main__":
    main() 