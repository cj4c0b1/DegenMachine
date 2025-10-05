# Apply patches before any other imports
import patch_parsimonious  # noqa: F401
import patch_frozendict  # noqa: F401

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

class MockClient:
    def __init__(self, private_key, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        self.private_key = private_key
        self.chain_id = 324  # zkSync Era chain ID
        self.network = 'zksync'
        
    async def prepare_transaction(self):
        nonce = self.w3.eth.get_transaction_count(self.address)
        return {
            'nonce': nonce,
            'chainId': self.chain_id,
        }
        
    async def check_for_approved(self, token_address, contract_address, amount):
        # Mock approval check - in a real scenario, this would check/approve token spending
        return True

async def main():
    # Configuration
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    if not PRIVATE_KEY:
        raise ValueError("PRIVATE_KEY not found in .env file")

    # Clean up the private key
    PRIVATE_KEY = PRIVATE_KEY.strip()  # Remove any whitespace

    # Remove 0x prefix if present (we'll add it back if needed)
    if PRIVATE_KEY.startswith('0x'):
        PRIVATE_KEY = PRIVATE_KEY[2:]

    # Validate private key format
    if not all(c in '0123456789abcdefABCDEF' for c in PRIVATE_KEY):
        raise ValueError("Private key contains invalid characters. It should only contain 0-9 and a-f (with or without 0x prefix)")

    if len(PRIVATE_KEY) != 64:
        raise ValueError(f"Private key should be 64 characters long (32 bytes), got {len(PRIVATE_KEY)} characters")

    # Add 0x prefix for web3
    PRIVATE_KEY = '0x' + PRIVATE_KEY

    RPC_URL = "https://mainnet.era.zksync.io"  # zkSync Era mainnet RPC
    print("Using RPC URL:", RPC_URL)
    print(f"Using address: {Web3.to_checksum_address(PRIVATE_KEY[-40:])}")
    
    # Initialize client
    client = MockClient(PRIVATE_KEY, RPC_URL)
    
    # Import OpenOcean after client is defined to avoid circular imports
    from modules.swaps.openocean import OpenOcean
    
    # Initialize OpenOcean
    openocean = OpenOcean(client)
    
    try:
        # Test with a small amount of ETH to USDC swap (0.001 ETH)
        print("\nTesting OpenOcean swap...")
        print("From: ETH")
        print("To: USDC")
        print("Amount: 0.001 ETH")
        
        # Get ETH balance before swap
        eth_balance = client.w3.eth.get_balance(client.address)
        print(f"ETH balance before: {Web3.from_wei(eth_balance, 'ether')} ETH")
        
        # Execute the swap
        result = await openocean.swap(
            swapdata=("ETH", "USDC", 0.001, 10**15)  # 0.001 ETH to USDC
        )
        
        if hasattr(result, 'hex'):
            tx_hash = result.hex()
        else:
            tx_hash = result
            
        print(f"\nSwap successful! Transaction hash: {tx_hash}")
        
        # Get ETH balance after swap
        eth_balance_after = client.w3.eth.get_balance(client.address)
        print(f"ETH balance after: {Web3.from_wei(eth_balance_after, 'ether')} ETH")
        
        return tx_hash
        
    except Exception as e:
        print(f"\nError during swap: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Check if running in a Jupyter notebook or IPython
    try:
        import nest_asyncio
        nest_asyncio.apply()
        print("Running in Jupyter/Colab environment - applied nest_asyncio")
    except (ImportError, ModuleNotFoundError):
        pass
    
    # Run the main async function
    asyncio.run(main())
