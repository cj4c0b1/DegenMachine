# Apply patches before any other imports
import patch_parsimonious_fix  # noqa: F401
import patch_frozendict_fix  # noqa: F401
import patch_starkware  # noqa: F401

import asyncio
import os
import sys
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Mock Client class to avoid Starknet dependencies
class MockClient:
    def __init__(self, private_key, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        self.private_key = private_key
        self.network = type('Network', (), {'name': 'zksync', 'token': 'ETH'})
        self.chain_id = 324  # zkSync Era chain ID

    def get_contract(self, address, abi):
        return self.w3.eth.contract(address=address, abi=abi)

    async def prepare_transaction(self, value=0):
        nonce = self.w3.eth.get_transaction_count(self.address)
        gas_price = self.w3.eth.gas_price
        
        return {
            'chainId': self.chain_id,
            'gas': 300000,  # Default gas limit
            'gasPrice': gas_price,
            'nonce': nonce,
            'value': value,
            'from': self.address,
        }

    async def send_transaction(self, transaction):
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.to_hex(tx_hash)

# Import OpenOcean directly to avoid importing Starknet dependencies
from modules.swaps.openocean import OpenOcean

# Remove the StarknetClient from modules to prevent it from being imported
import sys
if 'modules.stark_client' in sys.modules:
    del sys.modules['modules.stark_client']
if 'starknet_py' in sys.modules:
    del sys.modules['starknet_py']

async def main():
    # Get private key from environment variable
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("Error: PRIVATE_KEY environment variable not set")
        return

    # Initialize Web3 client
    rpc_url = "https://mainnet.era.zksync.io"  # zkSync Era RPC URL
    client = MockClient(private_key, rpc_url)
    
    # Initialize OpenOcean
    openocean = OpenOcean(client)
    
    # Token addresses (example: ETH to USDC on zkSync Era)
    from_token_address = '0x0000000000000000000000000000000000000000'  # ETH
    to_token_address = '0x3355df6D000c7e3d8780a2343C0a87b40497eB9B'  # USDC on zkSync
    
    # Amount to swap (in wei)
    amount_wei = Web3.to_wei(0.001, 'ether')  # 0.001 ETH
    
    try:
        print(f"Building swap transaction for {Web3.from_wei(amount_wei, 'ether')} ETH to USDC...")
        
        # Build the swap transaction
        transaction = await openocean.build_swap_transaction(
            from_token_address=from_token_address,
            to_token_address=to_token_address,
            amount=amount_wei
        )
        
        print("Transaction built successfully!")
        print(f"From: {transaction['from']}")
        print(f"To: {transaction['to']}")
        print(f"Value: {Web3.from_wei(transaction['value'], 'ether')} ETH")
        print(f"Gas: {transaction['gas']}")
        print(f"Gas Price: {Web3.from_wei(transaction['gasPrice'], 'gwei')} Gwei")
        
        # Uncomment to send the transaction
        # print("\nSending transaction...")
        # tx_hash = await client.send_transaction(transaction)
        # print(f"Transaction sent! Hash: {tx_hash}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
