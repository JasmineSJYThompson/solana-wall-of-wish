# Solana Wall of Wish

A decentralized wish wall application built on the Solana blockchain. The program is built and deployed using the Solana Playground, and this repository contains the frontend code to interact with it.

## Features

- Submit wishes to the Solana blockchain
- View all wishes stored on-chain
- Decode and display wish data from the blockchain
- Simple and intuitive interface

## Project Structure

```
solana-wall-of-wish/
├── app.py              # Streamlit frontend application
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Solana Playground account

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

1. Deploy your program on the Solana Playground
2. Start the Streamlit app:
```bash
streamlit run streamlit_decode_data.py
```
3. Open your browser and navigate to `http://localhost:8501`
4. Enter your Solana public key and start submitting wishes!

## How It Works

### Frontend (app.py)
- Streamlit application for user interaction
- Simple interface for submitting and viewing wishes
- Displays decoded wish data from the blockchain

### Data Structure
Each wish is stored on the blockchain with the following structure:
- Author's public key
- Timestamp
- Wish title/content

## Development

The Solana program must be built and deployed using the Solana Playground. Follow these steps:

1. Visit [Solana Playground](https://beta.solpg.io/)
2. Create a new project
3. Write and deploy your program
4. Use the deployed program ID in the frontend application

## Security

- Never share your private keys
- Always verify wallet addresses
- Use environment variables for sensitive information

## License

MIT License 