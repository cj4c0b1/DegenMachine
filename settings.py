"""
--------------------------------------------------OKX CONTROL-----------------------------------------------------------
    Select networks/amounts for OKX withdrawals and deposits. Don't forget to insert your API keys below.

    1 - ETH-ERC20              9  - CELO-Celo           17 - KLAY-Klaytn        26 - USDT-Arbitrum One
    2 - ETH-Arbitrum One       10 - ONE-Harmony         18 - FTM-Fantom         27 - USDC-ERC20
    3 - ETH-zkSync Lite        11 - GLMR-Moonbeam       19 - AVAX-Avalanche     28 - USDC-Optimism
    4 - ETH-Optimism           12 - MOVR-Moonriver      20 - ASTR-Astar         29 - USDC-Avalanche
    5 - ETH-Starknet           13 - METIS-Metis         21 - BNB-BSC            30 - USDC-Arbitrum One
    6 - ETH-zkSync Era         14 - CORE-CORE           22 - MATIC-Polygon      31 - USDC-Polygon
    7 - ETH-Linea              15 - CFX-Conflux         23 - USDT-Polygon       32 - USDC-Polygon (Bridged)
    8 - ETH-Base               16 - ZEN-Horizen         24 - USDT-Optimism      33 - USDC-Optimism (Bridged)
                                                        25 - USDT-Avalanche     34 - USDT-ERC20

------------------------------------------------------------------------------------------------------------------------
"""
OKX_WITHDRAW_NETWORK = 22      # Withdrawal network from OKX
OKX_WITHDRAW_AMOUNT = (1, 1)   # (min, max) amount for OKX withdrawal (quantity)

OKX_MULTI_WITHDRAW = {  # Withdrawal network: (min, max) in token for withdrawal (quantity)
    9: (1, 1.011),
    4: (0.0001, 0.000111),
}

OKX_DEPOSIT_NETWORK = 32                  # Network for OKX deposit
OKX_DEPOSIT_AMOUNT = ('100', '100')    # (min, max) amount for OKX deposit (% or quantity)

"""
------------------------------------------------BRIDGE CONTROL----------------------------------------------------------
    Please verify manually if the network is working on the website. (The software will check, but why stress it?)
    The software works only with the native token (ETH). Don't forget to insert your LayerSwap API key.
    Each bridge supports unique configuration
    
    You can specify min/max amount or min/max % of balance
    
    Amount - (0.01, 0.02)
    Percentage - ("10", "20") ⚠️ Values in brackets
       
     (A)Arbitrum = 1                    Polygon ZKEVM = 10 
        Arbitrum Nova = 2            (A)zkSync Era = 11     
     (A)Base = 3                       *Zora = 12 
        Linea = 4                       Ethereum = 13
        Manta = 5                      *Avalanche = 14
       *Polygon = 6                     BNB Chain = 15
     (A)Optimism = 7                 (O)Metis = 26        
        Scroll = 8                     *OpBNB = 28
        Starknet = 9                   *Mantle = 29
                                        ZKFair = 45   
    
    * - not supported in Rhino.fi
    (A) - networks supported by Across bridge
    (0) - supported only for Orbiter bridge
    ORBITER_CHAIN_ID_FROM(TO) = [2, 4, 16] | One of the networks will be selected
"""

ORBITER_CHAIN_ID_FROM = [7]                # Source network
ORBITER_CHAIN_ID_TO = [45]                # Destination network
ORBITER_DEPOSIT_AMOUNT = (1, 1)          # (min, max) (% or quantity)
ORBITER_TOKEN_NAME = 'USDC'

LAYERSWAP_CHAIN_ID_FROM = [1]                # Source network
LAYERSWAP_CHAIN_ID_TO = [4]                  # Destination network
LAYERSWAP_DEPOSIT_AMOUNT = (0.002, 0.002)    # (min, max) (% or quantity)

RHINO_CHAIN_ID_FROM = [1]                # Source network
RHINO_CHAIN_ID_TO = [11]                  # Destination network
RHINO_DEPOSIT_AMOUNT = (0.012, 0.022)    # (min, max) (% or quantity)

ACROSS_CHAIN_ID_FROM = [9]                # Source network
ACROSS_CHAIN_ID_TO = [4]                  # Destination network
ACROSS_DEPOSIT_AMOUNT = (0.002, 0.002)    # (min, max) (% or quantity)

"""
--------------------------------------------------DEGEN SETTINGS--------------------------------------------------------
    
    Supported networks for module operation. Before configuration, check if the website works with the specified network!
    
        Arbitrum = 1                  Goerli = 16                        OKX = 30
        Arbitrum Nova = 2             Gnosis = 17                        Optimism = 31
        Astar = 3                     Harmony = 18                       Orderly = 32
        Aurora = 4                    Horizen = 19                       Polygon = 33  
        Avalanche = 5                 Kava = 20                          Polygon zkEVM = 34
        BNB = 6                       Klaytn = 21                        Scroll = 35
        Base = 7                      Linea = 22                         ShimmerEVM = 36
        Canto = 8                     Loot = 23                          Telos = 37
        Celo = 9                      Manta = 24                         TomoChain = 38 
        Conflux = 10                  Mantle = 25                        Tenet = 39
        CoreDAO = 11                  Meter = 26                         XPLA = 40
        DFK = 12                      Metis = 27                         Zora = 41  
        Ethereum = 13                 Moonbeam = 28                      opBNB = 42
        Fantom = 14                   Moonriver = 29                     zkSync = 43
        Fuse = 15                                                        Beam = 44
            
    INSCRIPTION_DATA | Specify the data for minting. Usually provided on the websites. Supported formats are json and hex.
        In json format - 'data....'
        In hex format - 0x123
    INSCRIPTION_NETWORK | Network where the inscription will be minted. All networks from OMNI-CHAIN CONTROL are supported.
    
    MEMCOIN_AMOUNT | Amount in ETH you plan to spend on memcoin purchase.
"""
INSCRIPTION_DATA = ''  # Json или Hex формат
INSCRIPTION_NETWORK = 1  # network for Inscription mint (numbers from DEGEN SETTINGS)
INSCRIPTION_NETWORK_ORBITER = 7  # destination network for Orbiter Inscription (numbers from DEGEN SETTINGS)

MEMCOIN_AMOUNT = 0.01  # сумма в ETH

ZKFAIR_STAKE_PERIOD = 90  # number of days for staking (month = 30)
ZKFAIR_STAKE_AMOUNT = 50  # percentage of ZKF balance for staking
ZKFAIR_CLAIM_REFUND_PHASES = [1, 2, 3, 4]  # phases for refund claim


"""
--------------------------------------------CLASSIC-ROUTES CONTROL------------------------------------------------------

---------------------------------------------------HELPERS--------------------------------------------------------------        

    okx_withdraw                     # see OKX CONTROL
    okx_multi_withdraw               # withdraw to multiple networks. See OKX CONTROL (OKX_MULTI_WITHDRAW)
    collector_eth                    # collect all tokens to ETH
    bridge_across                    # see BRIDGE CONTROL
    bridge_rhino                     # see BRIDGE CONTROL
    bridge_layerswap                 # see BRIDGE CONTROL
    bridge_orbiter                   # see BRIDGE CONTROL
    okx_deposit                      # deposit funds to exchange
    okx_collect_from_sub             # collect funds from sub-accounts to main account
    
---------------------------------------------------CUSTOM---------------------------------------------------------------        
    
    mint_token_avnu                  # exchange shield for AVNU. see MEMCOIN_AMOUNT. Change contract in config.py -> TOKENS_PER_CHAIN
    mint_scroll_nft                  # mint Scroll NFT for contract deployment
    mint_inscription                 # mint inscription in INSCRIPTION_NETWORK (numbers from L0).
    mint_orbiter_inscription         # mint inscription on Orbiter, see INSCRIPTION_NETWORK, INSCRIPTION_NETWORK_ORBITER.
    zksync_rhino_checker             # check eligibility for Rhino.fi Pro Hunter NFT mint
    zksync_rhino_mint                # mint Rhino.fi Hunter NFT
    zksync_rhino_mint_pro            # check eligibility and mint Rhino.fi Pro Hunter NFT
    claim_refund_zkfair              # claim refund for participating in ZKFair airdrop, see ZKFAIR_CLAIM_REFUND_PHASES
    stake_zkfair                     # stake ZKF token on ZKFair network, see ZKFAIR_STAKE_PERIOD, ZKFAIR_STAKE_AMOUNT

    Select the necessary modules for interaction
    You can create any route, the software will follow it strictly. For each list, one module will be selected for
    the route. If the software selects None, it will skip that module list.
    Module list is above.
    
    CLASSIC_ROUTES_MODULES_USING = [
        ['okx_withdraw'],
        ['bridge_layerswap', 'bridge_oribter', None],
        ['stake_zkfair', 'zksync_rhino_mint_pro']
        ...
    ]
"""
CLASSIC_ROUTES_MODULES_USING = [
    ['okx_withdraw'],
    ['bridge_layerswap', 'bridge_oribter', None],
    ['stake_zkfair', 'zksync_rhino_mint_pro']
]
