#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import time
from web3 import AsyncWeb3
from web3.middleware import async_gas_price_strategy
from config import TOKENS_PER_CHAIN, ETH_MASK
from modules.client import Client
from utils.networks import Network

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get network from environment or use Base as default
NETWORK_NAME = os.getenv('NETWORK', 'Base')

# Import the specific network RPC
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.networks import BaseRPC  # Import the specific network RPC

# Use the imported network
NETWORK = BaseRPC  # Default to BaseRPC

print(f"🔧 Using network: {NETWORK_NAME}")
print(f"🆔 Chain ID: {NETWORK.chain_id}")
print(f"🔍 Explorer: {NETWORK.explorer}")
print(f"💎 Native Token: {NETWORK.token}")
print("-" * 50)

# Available RPC endpoints for testing
RPC_ENDPOINTS = [
    'https://rpc.ankr.com/base',
    'https://base.llamarpc.com',
    'https://base.drpc.org',
    'https://1rpc.io/base',
    'https://mainnet.base.org',
    'https://base.publicnode.com',
    'https://base.blockpi.network/v1/rpc/public',
    'https://base.meowrpc.com'
]

async def test_rpc_connection(rpc_url):
    """Test the RPC connection and get basic info"""
    print(f"\n🔍 Testing RPC: {rpc_url}")
    
    # Add request timeout and retry logic
    request_kwargs = {
        'timeout': 10,  # 10 second timeout
        'request_kwargs': {
            'headers': {
                'Content-Type': 'application/json',
                'User-Agent': 'DegenMachine/1.0'
            }
        }
    }
    
    try:
        # Initialize Web3 with the RPC provider
        provider = AsyncWeb3.AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs)
        w3 = AsyncWeb3(provider)
        
        # Add middleware for better error handling
        w3.middleware_onion.inject(async_gas_price_strategy, layer=0)
        
        # Test connection with timeout
        start_time = time.time()
        is_connected = await asyncio.wait_for(w3.is_connected(), timeout=10)
        response_time = (time.time() - start_time) * 1000  # in milliseconds
        
        if is_connected:
            print(f"✅ Connected in {response_time:.0f}ms")
            
            # Get network info with timeout
            try:
                start_time = time.time()
                chain_id = await asyncio.wait_for(w3.eth.chain_id, timeout=10)
                block_number = await asyncio.wait_for(w3.eth.block_number, timeout=10)
                gas_price = await asyncio.wait_for(w3.eth.gas_price, timeout=10)
                
                print(f"   📡 Network ID: {chain_id}")
                print(f"   📦 Latest block: {block_number}")
                print(f"   ⛽ Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")
                
                # Get syncing status
                try:
                    sync_status = await asyncio.wait_for(w3.eth.syncing, timeout=5)
                    if sync_status:
                        print("   ⚠️  Node is still syncing! This might cause issues.")
                        if hasattr(sync_status, 'currentBlock'):
                            print(f"   Current block: {sync_status.currentBlock}")
                            print(f"   Highest block: {sync_status.highestBlock}")
                        else:
                            print(f"   Sync status: {sync_status}")
                    else:
                        print("   ✅ Node is fully synced")
                except asyncio.TimeoutError:
                    print("   ⚠️  Timeout checking sync status")
                except Exception as e:
                    print(f"   ⚠️  Could not get sync status: {e}")
                
                return {
                    'url': rpc_url,
                    'connected': True,
                    'response_time': response_time,
                    'chain_id': chain_id,
                    'block_number': block_number,
                    'gas_price': gas_price,
                    'w3': w3
                }
                
            except asyncio.TimeoutError:
                print("   ⚠️  Timeout getting network info")
                return {
                    'url': rpc_url,
                    'connected': False,
                    'error': 'Timeout getting network info',
                    'response_time': response_time
                }
            except Exception as e:
                print(f"   ⚠️  Error getting network info: {e}")
                return {
                    'url': rpc_url,
                    'connected': False,
                    'error': str(e),
                    'response_time': response_time
                }
        
        return {
            'url': rpc_url,
            'connected': False,
            'error': 'Failed to connect',
            'response_time': response_time
        }
        
    except asyncio.TimeoutError:
        print(f"   ❌ Connection timed out after 10s")
        return {
            'url': rpc_url,
            'connected': False,
            'error': 'Connection timeout',
            'response_time': 10000  # 10s in ms
        }
    except Exception as e:
        print(f"   ❌ Failed to connect: {e}")
        return {
            'url': rpc_url,
            'connected': False,
            'error': str(e),
            'response_time': None
        }

async def find_best_rpc():
    """Test all RPC endpoints and return the best one"""
    print("\n🔍 Testing all available RPC endpoints...")
    
    # Test all RPC endpoints in parallel
    tasks = [test_rpc_connection(url) for url in RPC_ENDPOINTS]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and sort by response time
    valid_results = [r for r in results if isinstance(r, dict) and r.get('connected', False)]
    valid_results.sort(key=lambda x: x.get('response_time', float('inf')))
    
    print("\n📊 RPC Endpoint Test Results:")
    print("-" * 80)
    
    # Print all results
    for i, result in enumerate(valid_results + [r for r in results if isinstance(r, dict) and not r.get('connected', False)]):
        status = "✅" if result.get('connected', False) else "❌"
        time_str = f"{result.get('response_time', 0):.0f}ms" if result.get('response_time') else "timeout"
        print(f"{i+1}. {status} {result['url']} ({time_str})")
        if 'chain_id' in result:
            print(f"   Chain ID: {result['chain_id']}, Block: {result.get('block_number', 'N/A')}, Gas: {result.get('gas_price', 'N/A')}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    print("-" * 80)
    
    # Return the best RPC (fastest valid one)
    if valid_results:
        best = valid_results[0]
        print(f"\n🏆 Best RPC: {best['url']} ({best.get('response_time', 0):.0f}ms)")
        return best['w3'], best['url']
    
    print("\n❌ No working RPC endpoints found!")
    return None, None

async def check_wallet_balance(w3, address):
    """Check the ETH balance of a wallet"""
    print(f"\n💰 Checking ETH balance for {address}")
    try:
        balance = await w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"   Balance: {balance_eth:.6f} ETH")
        return balance
    except Exception as e:
        print(f"❌ Error getting balance: {e}")
        return 0

async def check_token_balance(w3, token_address, token_name, wallet_address):
    """Check the balance of a specific token for a wallet"""
    print(f"\n🔍 Checking {token_name} balance...")
    print(f"   Token address: {token_address}")
    
    try:
        # Basic ERC20 ABI with just the functions we need
        erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            }
        ]
        
        # Create contract instance
        contract = w3.eth.contract(
            address=w3.to_checksum_address(token_address),
            abi=erc20_abi
        )
        
        # Get token info
        try:
            symbol = await contract.functions.symbol().call()
            print(f"   Token symbol: {symbol}")
        except:
            symbol = token_name
            print(f"   Could not get token symbol, using provided name: {token_name}")
        
        # Get decimals
        try:
            decimals = await contract.functions.decimals().call()
            print(f"   Token decimals: {decimals}")
        except Exception as e:
            print(f"⚠️  Could not get token decimals: {e}")
            decimals = 18  # Default to 18 decimals
        
        # Get balance
        balance = await contract.functions.balanceOf(wallet_address).call()
        normalized_balance = balance / (10 ** decimals)
        
        print(f"   Balance: {normalized_balance:.6f} {symbol}")
        return balance
        
    except Exception as e:
        print(f"❌ Error checking {token_name} balance: {e}")
        return 0

async def main():
    print("\n🔧 DegenMachine RPC & Balances Diagnostic Tool 🔧")
    print("=" * 50)
    
    # Find the best working RPC endpoint
    w3, best_rpc = await find_best_rpc()
    
    if not w3 or not best_rpc:
        print("\n❌ No working RPC endpoints found. Please check your internet connection or try again later.")
        return
    
    print(f"\n🌐 Using RPC: {best_rpc}")
    
    # Get network info
    chain_id = await w3.eth.chain_id
    block_number = await w3.eth.block_number
    gas_price = await w3.eth.gas_price
    
    print(f"\n📡 Network Info:")
    print(f"   Chain ID: {chain_id}")
    print(f"   Latest block: {block_number}")
    print(f"   Gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")
    
    # Get wallet address for balance checking
    private_key = input("\n🔑 Enter your private key (or leave empty to skip balance checks): ").strip()
    
    if not private_key:
        print("\nℹ️  Skipping wallet balance checks.")
        return
    
    # Create a client to get the address
    client = Client("diagnostic", private_key, NETWORK)
    wallet_address = client.address
    print(f"\n👛 Wallet address: {wallet_address}")
    
    # Check ETH balance
    eth_balance = await check_wallet_balance(w3, wallet_address)
    
    # Check token balances
    print("\n📊 Checking token balances...")
    network_name = NETWORK.name
    
    if network_name in TOKENS_PER_CHAIN:
        tokens = TOKENS_PER_CHAIN[network_name]
        print(f"\nFound {len(tokens)} tokens for {network_name} network")
        
        for token_name, token_address in tokens.items():
            if token_name == 'ETH':
                continue  # Already checked ETH balance
                    
                # Skip if token address is the same as ETH_MASK
                if token_address == ETH_MASK:
                    print(f"\n⚠️  {token_name} address is the same as ETH_MASK, skipping...")
                    continue
                    
                await check_token_balance(w3, token_address, token_name, wallet_address)
                await asyncio.sleep(0.5)  # Rate limiting
        else:
            print(f"\n❌ No token configuration found for {network_name} network")
    
    # Test contract interactions
    print("\n🧪 Testing contract interactions...")
    
    # Test a simple contract call (e.g., WETH contract on Base)
    if network_name == 'Base':
        print("\n🔍 Testing WETH contract interaction...")
        weth_address = TOKENS_PER_CHAIN.get('Base', {}).get('WETH')
        if weth_address:
            try:
                # Simple call to check if the contract is responsive
                weth_contract = w3.eth.contract(
                    address=w3.to_checksum_address(weth_address),
                    abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"}]
                )
                name = await weth_contract.functions.name().call()
                print(f"✅ Successfully called WETH contract. Name: {name}")
            except Exception as e:
                print(f"❌ Error calling WETH contract: {e}")
    
    print("\n✅ Diagnostic complete!")

if __name__ == "__main__":
    asyncio.run(main())
