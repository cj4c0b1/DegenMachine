"""
Standalone OpenOcean integration for token swaps.

This module provides a simple interface to interact with OpenOcean's API
for token swaps on EVM-compatible blockchains.
"""

import asyncio
import aiohttp
from web3 import Web3
from web3.middleware import geth_poa_middleware
from typing import Dict, Any, Optional

class OpenOceanStandalone:
    """
    A standalone implementation of OpenOcean aggregator without Starknet dependencies.
    
    This class provides functionality to get quotes and execute token swaps
    using OpenOcean's aggregation protocol.
    """
    
    def __init__(self, private_key: str, rpc_url: str, chain_id: int = 324):
        """
        Initialize the OpenOcean client.
        
        Args:
            private_key: The private key for the wallet
            rpc_url: The RPC URL for the blockchain network
            chain_id: The chain ID of the network (default: 324 for zkSync Era)
        """
        self.private_key = private_key
        self.chain_id = chain_id
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if 'goerli' in rpc_url or 'testnet' in rpc_url:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Set up account
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        
        # API settings
        self.api_url = 'https://open-api.openocean.finance/v3'
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        }

class OpenOceanStandalone:
    """
    A standalone implementation of OpenOcean aggregator without Starknet dependencies.
    """
    
    def __init__(self, private_key: str, rpc_url: str, chain_id: int = 324):
        """
        Initialize the OpenOcean client.
        
        Args:
            private_key: The private key for the wallet
            rpc_url: The RPC URL for the blockchain network
            chain_id: The chain ID of the network (default: 324 for zkSync Era)
        """
        self.private_key = private_key
        self.chain_id = chain_id
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if 'goerli' in rpc_url or 'testnet' in rpc_url:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Set up account
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        
        # API settings
        self.api_url = 'https://open-api.openocean.finance/v3'
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def get_quote(
        self, 
        from_token_address: str, 
        to_token_address: str, 
        amount: int,
        slippage: float = 1.0
    ) -> Dict[str, Any]:
        """
        Get a quote for a token swap.
        
        Args:
            from_token_address: The token address to swap from (use '0x0000000000000000000000000000000000000000' for native token)
            to_token_address: The token address to swap to
            amount: The amount to swap in wei
            slippage: The maximum slippage percentage (default: 1.0%)
            
        Returns:
            Dictionary containing the quote details
        """
        url = f"{self.api_url}/{self.chain_id}/quote"
        
        # Get current gas price
        gas_price = await self.w3.eth.gas_price
        
        params = {
            'inTokenAddress': from_token_address,
            'outTokenAddress': to_token_address,
            'amount': str(amount),
            'gasPrice': str(Web3.from_wei(gas_price, 'gwei')),
            'slippage': str(slippage),
            'account': self.address.lower()
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get quote: {error_text}")
                return await response.json()
    
    async def get_swap_data(
        self, 
        from_token_address: str, 
        to_token_address: str, 
        amount: int,
        slippage: float = 1.0
    ) -> Dict[str, Any]:
        """
        Get swap data including transaction parameters.
        
        Args:
            from_token_address: The token address to swap from (use '0x0000000000000000000000000000000000000000' for native token)
            to_token_address: The token address to swap to
            amount: The amount to swap in wei
            slippage: The maximum slippage percentage (default: 1.0%)
            
        Returns:
            Dictionary containing the swap data including transaction parameters
        ""
        url = f"{self.api_url}/{self.chain_id}/swap_quote"
        
        # Get gas parameters
        gas_price = await self.w3.eth.gas_price
        
        # For EIP-1559 transactions (like zkSync Era)
        if self.chain_id in [324]:  # zkSync Era
            latest_block = await self.w3.eth.get_block('latest')
            base_fee = latest_block['baseFeePerGas']
            priority_fee_wei = Web3.to_wei(0.1, 'gwei')  # Fixed priority fee for zkSync
            max_fee_per_gas = base_fee + priority_fee_wei
            
            params = {
                'chain': self.chain_id,
                'inTokenAddress': from_token_address,
                'outTokenAddress': to_token_address,
                'amount': str(amount),
                'maxFeePerGas': str(Web3.from_wei(max_fee_per_gas, 'gwei')),
                'maxPriorityFeePerGas': str(Web3.from_wei(priority_fee_wei, 'gwei')),
                'slippage': str(slippage),
                'account': self.address.lower(),
                'type': '0x2'  # EIP-1559 transaction type
            }
        else:
            # For legacy transactions
            params = {
                'chain': self.chain_id,
                'inTokenAddress': from_token_address,
                'outTokenAddress': to_token_address,
                'amount': str(amount),
                'gasPrice': str(Web3.from_wei(gas_price, 'gwei')),
                'slippage': str(slippage),
                'account': self.address.lower()
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get swap data: {error_text}")
                return await response.json()
    
    async def build_swap_transaction(
        self, 
        from_token_address: str, 
        to_token_address: str, 
        amount: int,
        slippage: float = 1.0
    ) -> Dict[str, Any]:
        """
        Build a swap transaction.
        
        Args:
            from_token_address: The token address to swap from (use '0x0000000000000000000000000000000000000000' for native token)
            to_token_address: The token address to swap to
            amount: The amount to swap in wei
            slippage: The maximum slippage percentage (default: 1.0%)
            
        Returns:
            Dictionary containing the transaction parameters
        """
        # Get swap data from OpenOcean API
        swap_data = await self.get_swap_data(from_token_address, to_token_address, amount, slippage)
        
        # Prepare transaction parameters
        nonce = await self.w3.eth.get_transaction_count(self.address)
        gas_price = await self.w3.eth.gas_price
        
        tx_params = {
            'chainId': self.chain_id,
            'from': self.address,
            'to': self.w3.to_checksum_address(swap_data['to']),
            'data': swap_data['data'],
            'value': int(swap_data['value']),
            'gas': int(swap_data['estimatedGas']),
            'gasPrice': gas_price,
            'nonce': nonce,
        }
        
        # For EIP-1559 transactions
        if 'maxFeePerGas' in swap_data and 'maxPriorityFeePerGas' in swap_data:
            tx_params['maxFeePerGas'] = Web3.to_wei(float(swap_data['maxFeePerGas']), 'gwei')
            tx_params['maxPriorityFeePerGas'] = Web3.to_wei(float(swap_data['maxPriorityFeePerGas']), 'gwei')
            tx_params.pop('gasPrice', None)  # Remove gasPrice for EIP-1559
        
        return tx_params
    
    async def execute_swap(
        self, 
        from_token_address: str, 
        to_token_address: str, 
        amount: int,
        slippage: float = 1.0
    ) -> str:
        """
        Execute a token swap.
        
        Args:
            from_token_address: The token address to swap from (use '0x0000000000000000000000000000000000000000' for native token)
            to_token_address: The token address to swap to
            amount: The amount to swap in wei
            slippage: The maximum slippage percentage (default: 1.0%)
            
        Returns:
            Transaction hash as a hex string
        """

        # Build the transaction
        tx_params = await self.build_swap_transaction(from_token_address, to_token_address, amount, slippage)
        
        # Sign and send the transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return self.w3.to_hex(tx_hash)

# Example usage
async def example_swap():
    # Configuration
    PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Never hardcode in production
    RPC_URL = "https://mainnet.era.zksync.io"  # zkSync Era RPC
    
    # Initialize client
    client = OpenOceanStandalone(
        private_key=PRIVATE_KEY,
        rpc_url=RPC_URL,
        chain_id=324  # zkSync Era
    )
    
    # Token addresses (example: ETH to USDC on zkSync Era)
    ETH_ADDRESS = '0x0000000000000000000000000000000000000000'  # Native token (ETH)
    USDC_ADDRESS = '0x3355df6D000c7e3d8780a2343C0a87b40497eB9B'  # USDC on zkSync
    
    # Amount to swap (0.001 ETH in wei)
    amount = Web3.to_wei(0.001, 'ether')
    
    try:
        # Get a quote first
        quote = await client.get_quote(ETH_ADDRESS, USDC_ADDRESS, amount)
        print(f"Quote: {Web3.from_wei(int(quote['outAmount']), 6)} USDC for {Web3.from_wei(amount, 'ether')} ETH")
        
        # Execute the swap (uncomment to actually send the transaction)
        # tx_hash = await client.execute_swap(ETH_ADDRESS, USDC_ADDRESS, amount)
        # print(f"Swap executed! Transaction hash: {tx_hash}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(example_swap())
