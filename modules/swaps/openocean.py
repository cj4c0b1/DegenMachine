from modules import Aggregator, Logger
from utils.tools import gas_checker, helper
from general_settings import SLIPPAGE
from config import TOKENS_PER_CHAIN, ETH_MASK, HELP_SOFTWARE


class OpenOcean(Aggregator, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        Aggregator.__init__(self, client)
        self.network = self.client.network.name

    async def build_swap_transaction(self, from_token_address: str, to_token_address: str, amount: float):

        url = f'https://open-api.openocean.finance/v3/{self.client.chain_id}/swap_quote'

        params = {
            'chain': self.client.chain_id,
            'inTokenAddress': from_token_address,
            'outTokenAddress': to_token_address,
            'amount': f"{amount}",
            'gasPrice': str(self.client.w3.from_wei(await self.client.w3.eth.gas_price, 'gwei')),
            'slippage': SLIPPAGE,
            'account': self.client.address
        } | ({'referrer': '0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5', 'referrerFee': 1} if HELP_SOFTWARE else {})

        return await self.make_request(url=url, params=params)

    @helper
    @gas_checker
    async def swap(self, help_deposit: bool = False, swapdata: dict = None):
        try:
            # Log the start of the swap process
            self.logger_msg(
                *self.client.acc_info,
                msg=f"🚀 Starting swap process on {self.network} network",
                type_msg='info'
            )
            
            # Get swap parameters
            if not swapdata:
                self.logger_msg(
                    *self.client.acc_info,
                    msg="🔍 Getting automatic swap parameters...",
                    type_msg='info'
                )
                try:
                    from_token_name, to_token_name, amount, amount_in_wei = await self.client.get_auto_amount()
                except RuntimeError as e:
                    if "No tokens with non-zero balance" in str(e):
                        self.logger_msg(
                            *self.client.acc_info,
                            msg="⚠️  No tokens with non-zero balance available for swapping",
                            type_msg='warning'
                        )
                        return False
                    raise
            else:
                self.logger_msg(
                    *self.client.acc_info,
                    msg="🔍 Using provided swap parameters...",
                    type_msg='info'
                )
                from_token_name, to_token_name, amount, amount_in_wei = swapdata
                
                # Additional check for manual swap data
                balance, _ = await self.client.get_token_balance(from_token_name, False)
                if balance <= 0:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"⚠️  Cannot swap {from_token_name}: balance is zero",
                        type_msg='warning'
                    )
                    return False

            if help_deposit:
                self.logger_msg(
                    *self.client.acc_info,
                    msg="💡 Help deposit mode: Output will be converted to ETH",
                    type_msg='info'
                )
                to_token_name = 'ETH'

            # Log token details
            self.logger_msg(
                *self.client.acc_info,
                msg=(
                    f"🔄 Swap Details:\n"
                    f"   • From: {amount:.6f} {from_token_name} (Wei: {amount_in_wei})\n"
                    f"   • To: {to_token_name}"
                ),
                type_msg='info'
            )

            # Get token addresses
            token_data = TOKENS_PER_CHAIN[self.network]
            from_token_address = ETH_MASK if from_token_name == "ETH" else token_data[from_token_name]
            to_token_address = ETH_MASK if to_token_name == "ETH" else token_data[to_token_name]
            
            self.logger_msg(*self.client.acc_info, 
                          msg=f"🔗 From token address: {from_token_address} ({from_token_name})", 
                          type_msg='info')
            self.logger_msg(*self.client.acc_info, 
                          msg=f"🔗 To token address: {to_token_address} ({to_token_name})", 
                          type_msg='info')

            # Get swap quote
            swap_quote_data = await self.build_swap_transaction(from_token_address, to_token_address, amount)
            if not swap_quote_data or 'data' not in swap_quote_data:
                raise ValueError("Invalid swap quote data received from OpenOcean")

            contract_address = self.client.w3.to_checksum_address(swap_quote_data["data"]["to"])

            # Handle token approval if needed
            if from_token_name != "ETH":
                self.logger_msg(*self.client.acc_info, 
                              msg=f"🔐 Checking token approval for {from_token_name}...", 
                              type_msg='info')
                
                # Get current allowance
                try:
                    contract = self.client.get_contract(from_token_address)
                    current_allowance = await contract.functions.allowance(
                        self.client.address, 
                        contract_address
                    ).call()
                    
                    self.logger_msg(*self.client.acc_info, 
                                  msg=f"📝 Current allowance: {current_allowance / (10 ** await contract.functions.decimals().call())} {from_token_name}", 
                                  type_msg='info')
                    
                    # Check and approve if needed
                    if current_allowance < amount_in_wei:
                        self.logger_msg(*self.client.acc_info, 
                                      msg=f"⚠️  Insufficient allowance. Approving {from_token_name}...", 
                                      type_msg='warning')
                        await self.client.check_for_approved(from_token_address, contract_address, amount_in_wei)
                        self.logger_msg(*self.client.acc_info, 
                                      msg=f"✅ Approval successful for {from_token_name}", 
                                      type_msg='success')
                    else:
                        self.logger_msg(*self.client.acc_info, 
                                      msg=f"✅ Sufficient allowance already set for {from_token_name}", 
                                      type_msg='success')
                except Exception as e:
                    self.logger_msg(*self.client.acc_info, 
                                  msg=f"❌ Error checking allowance for {from_token_name}: {str(e)}", 
                                  type_msg='error')
                    raise

            # Prepare transaction parameters
            self.logger_msg(*self.client.acc_info, 
                          msg=f"🛠️  Building transaction parameters...", 
                          type_msg='info')
            
            nonce = await self.client.w3.eth.get_transaction_count(self.client.address)
            value = int(swap_quote_data["data"]["value"])
            
            tx_params = {
                'chainId': self.client.chain_id,
                'nonce': nonce,
                'from': self.client.address,
                'to': contract_address,
                'data': swap_quote_data["data"]["data"],
                'value': value
            }
            
            self.logger_msg(*self.client.acc_info, 
                          msg=f"📄 Transaction parameters prepared:"
                              f"\n  • Nonce: {nonce}"
                              f"\n  • To: {contract_address}"
                              f"\n  • Value: {value} wei ({self.client.w3.from_wei(value, 'ether')} ETH)"
                              f"\n  • Data: {swap_quote_data['data']['data'][:100]}...", 
                          type_msg='info')

            # Get gas price
            if self.client.eip1559_support:
                fee_history = await self.client.w3.eth.fee_history(1, 'latest', [20, 50, 80])
                base_fee = fee_history['baseFeePerGas'][-1]
                max_priority_fee_per_gas = self.client.w3.to_wei(0.1, 'gwei')  # 0.1 Gwei priority fee
                max_fee_per_gas = base_fee + max_priority_fee_per_gas
                tx_params.update({
                    'maxFeePerGas': max_fee_per_gas,
                    'maxPriorityFeePerGas': max_priority_fee_per_gas,
                    'type': 2  # EIP-1559
                })
            else:
                tx_params['gasPrice'] = await self.client.w3.eth.gas_price

            # Estimate gas
            try:
                gas_estimate = await self.client.w3.eth.estimate_gas(tx_params)
                tx_params['gas'] = int(gas_estimate * 1.2)  # 20% buffer
            except Exception as e:
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Gas estimation failed: {str(e)}. Using default gas limit.", 
                              type_msg='warning')
                tx_params['gas'] = 500000  # Fallback gas limit

            # Sign and send transaction
            try:
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Preparing transaction with params: {tx_params}", 
                              type_msg='info')
                
                # First try the standard way
                signed_tx = self.client.w3.eth.account.sign_transaction(tx_params, self.client.private_key)
                
                # Try different ways to access the raw transaction
                if hasattr(signed_tx, 'rawTransaction'):
                    raw_tx = signed_tx.rawTransaction
                elif hasattr(signed_tx, 'raw_transaction'):
                    raw_tx = signed_tx.raw_transaction
                elif hasattr(signed_tx, 'raw'):
                    raw_tx = signed_tx.raw
                else:
                    # If we can't find the raw transaction, try to build it manually
                    from eth_account import Account
                    account = Account.from_key(self.client.private_key)
                    signed_tx = account.sign_transaction(tx_params)
                    raw_tx = signed_tx.rawTransaction
                
                # Ensure raw_tx is in the correct format
                if not isinstance(raw_tx, (str, bytes, bytearray)):
                    raw_tx = raw_tx.hex()
                if isinstance(raw_tx, str) and not raw_tx.startswith('0x'):
                    raw_tx = '0x' + raw_tx
                
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Sending transaction...", 
                              type_msg='info')
                
                # Send the raw transaction
                tx_hash = await self.client.w3.eth.send_raw_transaction(raw_tx)
                
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Transaction sent. Hash: {tx_hash.hex()}", 
                              type_msg='info')
                
            except Exception as sign_error:
                error_msg = f"Error signing transaction: {str(sign_error)}"
                self.logger_msg(*self.client.acc_info, 
                              msg=error_msg, 
                              type_msg='error')
                # Log the full error details for debugging
                import traceback
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Error details: {traceback.format_exc()}", 
                              type_msg='error')
                
                # Fallback to client's send_transaction method
                try:
                    self.logger_msg(*self.client.acc_info, 
                                  msg="Trying fallback send_transaction method...", 
                                  type_msg='warning')
                    tx_hash = await self.client.send_transaction(tx_params, need_hash=True)
                except Exception as fallback_error:
                    self.logger_msg(*self.client.acc_info, 
                                  msg=f"Fallback send_transaction also failed: {str(fallback_error)}", 
                                  type_msg='error')
                    return False
            
            # Wait for transaction receipt
            try:
                self.logger_msg(*self.client.acc_info, 
                              msg="Waiting for transaction receipt...", 
                              type_msg='info')
                
                receipt = await self.client.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
                
                if receipt.status == 1:
                    self.logger_msg(*self.client.acc_info, 
                                  msg=f"Transaction successful: {self.client.explorer}tx/{tx_hash.hex()}", 
                                  type_msg='success')
                    return True
                else:
                    error_msg = f"Transaction failed with status 0: {self.client.explorer}tx/{tx_hash.hex()}"
                    self.logger_msg(*self.client.acc_info, 
                                  msg=error_msg, 
                                  type_msg='error')
                    
                    # Try to get the transaction to see if there's more info
                    try:
                        tx = await self.client.w3.eth.get_transaction(tx_hash)
                        self.logger_msg(*self.client.acc_info, 
                                      msg=f"Transaction details: {tx}", 
                                      type_msg='error')
                    except Exception as tx_error:
                        self.logger_msg(*self.client.acc_info, 
                                      msg=f"Could not fetch transaction details: {str(tx_error)}", 
                                      type_msg='error')
                    
                    return False
                    
            except Exception as receipt_error:
                self.logger_msg(*self.client.acc_info, 
                              msg=f"Error waiting for transaction receipt: {str(receipt_error)}", 
                              type_msg='error')
                return False
                
        except Exception as e:
            error_msg = f"Error in swap: {str(e)}"
            self.logger_msg(*self.client.acc_info, 
                          msg=error_msg, 
                          type_msg='error')
            
            # Log the full traceback for debugging
            import traceback
            self.logger_msg(*self.client.acc_info, 
                          msg=f"Traceback: {traceback.format_exc()}", 
                          type_msg='error')
            
            return False
