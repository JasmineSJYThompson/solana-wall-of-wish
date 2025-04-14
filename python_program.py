from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionInstruction
from solana.system_program import SYS_PROGRAM_ID
from anchorpy import Program, Provider, Wallet, Idl
import json
import base58
import struct
import time

class WishProgram:
    def __init__(self, program_id: PublicKey, provider: Provider):
        self.program_id = program_id
        self.provider = provider
        self.client = provider.connection
        
    async def make_wish(self, title: str, author: Keypair):
        """Create a new wish on the blockchain"""
        # Generate PDA for the wish
        wish_seed = f"wish_{author.public_key()}_{int(time.time())}"
        [wish_pda, _] = PublicKey.find_program_address(
            [bytes(wish_seed, "utf-8")],
            self.program_id
        )
        
        # Calculate space needed for the wish account
        # 8 bytes for discriminator + 32 bytes for author + 8 bytes for timestamp + 4 bytes for string length + string length
        space = 8 + 32 + 8 + 4 + len(title)
        
        # Create the instruction data
        instruction_data = bytes([0])  # Instruction discriminator for make_wish
        instruction_data += struct.pack("<I", len(title))  # String length
        instruction_data += title.encode()  # Title string
        
        # Create the instruction
        instruction = TransactionInstruction(
            keys=[
                {"pubkey": wish_pda, "is_signer": False, "is_writable": True},
                {"pubkey": author.public_key(), "is_signer": True, "is_writable": True},
                {"pubkey": SYS_PROGRAM_ID, "is_signer": False, "is_writable": False}
            ],
            program_id=self.program_id,
            data=instruction_data
        )
        
        # Create and send the transaction
        transaction = Transaction()
        transaction.add(instruction)
        
        try:
            result = await self.provider.send(transaction, [author])
            return True, result
        except Exception as e:
            return False, str(e)
    
    async def get_wish(self, wish_pda: PublicKey):
        """Retrieve a wish from the blockchain"""
        try:
            account_info = await self.client.get_account_info(wish_pda)
            if not account_info.value:
                return None
            
            data = account_info.value.data
            # Parse the account data
            author = PublicKey(data[8:40])
            timestamp = struct.unpack("<q", data[40:48])[0]
            title_length = struct.unpack("<I", data[48:52])[0]
            title = data[52:52+title_length].decode()
            
            return {
                "title": title,
                "author": author,
                "timestamp": timestamp
            }
        except Exception as e:
            print(f"Error getting wish: {e}")
            return None

    async def get_all_wishes(self):
        """Get all wishes from the program"""
        try:
            # This would typically use a more efficient method in production
            # For example, using a PDA with a counter or index
            program_accounts = await self.client.get_program_accounts(self.program_id)
            wishes = []
            
            for account in program_accounts.value:
                wish = await self.get_wish(account.pubkey)
                if wish:
                    wishes.append(wish)
            
            return sorted(wishes, key=lambda x: x["timestamp"], reverse=True)
        except Exception as e:
            print(f"Error getting all wishes: {e}")
            return [] 