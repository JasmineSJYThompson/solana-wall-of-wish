# Solana Wall of Wish

A decentralized wish wall application built on the Solana blockchain using Python and Streamlit.

## Features

- Connect your Solana wallet
- Submit wishes to the blockchain
- View recent wishes from other users
- Decentralized and secure

## Prerequisites

- Python 3.8 or higher
- Solana wallet (e.g., Phantom, Solflare)
- Solana CLI tools (optional, for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd solana-wall-of-wish
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Connect your Solana wallet by entering your wallet address

4. Start submitting and viewing wishes!

## Development

To develop and test the application:

1. Set up a local Solana test validator (optional)
2. Update the RPC URL in `solana_integration.py` to point to your test validator
3. Deploy your Solana program and update the `program_id` in `solana_integration.py`

## Security

- Never share your private keys
- Always verify wallet addresses
- Use environment variables for sensitive information

## License

MIT License 