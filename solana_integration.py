from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
import base58
import json
from anchorpy import Program, Provider, Wallet
import asyncio
import time

class SolanaWishWall:
    def __init__(self, rpc_url="https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.program_id = PublicKey("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS")
        self.provider = None
        self.program = None
    
    async def initialize(self, wallet_keypair: Keypair):
        """Initialize the program connection with a wallet"""
        self.provider = Provider(self.client, Wallet(wallet_keypair))
        self.program = await Program.from_idl(
            json.loads(open("program/idl.json").read()),
            self.program_id,
            self.provider
        )
    
    async def submit_wish(self, wallet_address: str, wish_text: str):
        """
        Submit a wish to the Solana blockchain using the Anchor program
        """
        try:
            if not self.program:
                return False, "Program not initialized"
            
            # Generate a PDA for the wish
            wish_seed = f"wish_{wallet_address}_{int(time.time())}"
            [wish_pda, _] = PublicKey.find_program_address(
                [bytes(wish_seed, "utf-8")],
                self.program_id
            )
            
            # Submit the wish
            await self.program.rpc["make_wish"](
                wish_text,
                ctx={
                    "wish": wish_pda,
                    "author": PublicKey(wallet_address),
                    "system_program": PublicKey("11111111111111111111111111111111")
                }
            )
            
            return True, "Wish submitted successfully"
        except Exception as e:
            return False, str(e)
    
    async def get_recent_wishes(self, limit: int = 10):
        """
        Fetch recent wishes from the blockchain
        """
        try:
            if not self.program:
                return []
            
            # Get all wish accounts
            wishes = await self.program.account["Wish"].all()
            sorted_wishes = sorted(wishes, key=lambda x: x.account.timestamp, reverse=True)
            return sorted_wishes[:limit]
        except Exception as e:
            print(f"Error fetching wishes: {e}")
            return []

    def verify_wallet(self, wallet_address: str):
        """
        Verify if a wallet address is valid
        """
        try:
            PublicKey(wallet_address)
            return True
        except:
            return False 