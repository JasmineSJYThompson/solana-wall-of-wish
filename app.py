import streamlit as st
import requests

# Constants
BACKEND_URL = "http://localhost:8000"  # Change this to your deployed backend URL

def main():
    st.title("Solana Wall of Wish")
    st.write("A decentralized wish wall built on Solana blockchain")
    
    # Simple public key input
    public_key = st.text_input("Enter your Solana public key")
    
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
            st.error("Please enter your public key and write a wish first")
    
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
                        st.write(f"Time: {wish['timestamp']}")
            else:
                st.info("No wishes found. Be the first to make a wish!")
        else:
            st.error("Error fetching wishes")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 