"""
----------------------------------------------AMOUNT CONTROL------------------------------------------------------------
    Here you define the amount or percentage of tokens for swaps, adding liquidity, deposits, and transfers
    The software takes % only for ETH, other tokens are taken at 100% of the balance

    You can specify min/max amount or min/max % of the balance

    Amount - (0.01, 0.02)
    Percentage - ("55", "60") ⚠️ Values in parentheses

    AMOUNT_PERCENT | Specify only %, without quotes. Can be specified with up to 6 decimal places (99.123456, 99.654321).
                        ⚠️Other amount settings must be in quotes (if you want to work with %)⚠️
    MIN_BALANCE | Minimum balance for the account. With a lower balance, an error will occur: (Insufficient balance on account!)
"""
AMOUNT_PERCENT = (55, 60)  # Used for swaps
AMOUNT_PERCENT_WRAPS = (55, 60)  # Used for the wrap_abuser module
LIQUIDITY_AMOUNT = (0.001, 0.002)  # Used for adding liquidity, deposits, and wrapping ETH
TRANSFER_AMOUNT = ('99', '99')  # Used for transfers
MIN_BALANCE = 0.001  # Amount of ETH in the account

"""
------------------------------------------------GENERAL SETTINGS--------------------------------------------------------
    GLOBAL_NETWORK | Blockchain for main interaction ⚠️

    Arbitrum = 1            Optimism = 7
    Arbitrum Nova = 2       Scroll = 8
    Base = 3                Starknet = 9
    Linea = 4               Polygon ZKEVM = 10
    Manta = 5               zkSync Era = 11
    Polygon = 6             Zora = 12
                            Gnosis = 20

    WALLETS_TO_WORK = 0 | The software will take wallets from the table according to the rules described below
    0       = all wallets in a row
    3       = only wallet #3
    4, 20   = wallet #4 and #20
    [5, 25] = wallets from #5 to #25

    ACCOUNTS_IN_STREAM      | Number of wallets in the stream for execution. If there are 100 wallets in total, and you specify 10,
                                the software will make 10 runs of 10 wallets each
    CONTROL_TIMES_FOR_SLEEP | Number of checks after which a random sleep will be enabled for all accounts
                                at the moment when gas drops to MAXIMUM_GWEI and accounts will continue working

    EXCEL_PASSWORD          | Enables password prompt when starting the software. First set a password in the table
    EXCEL_PAGE_NAME         | Worksheet name in the table. Example: 'Starknet'

"""
GLOBAL_NETWORK = 11             # As of 26.12.2023 all networks from OMNI-CHAIN CONTROL are supported
SOFTWARE_MODE = 0               # 0 - sequential launch / 1 - parallel launch
ACCOUNTS_IN_STREAM = 1          # Only for SOFTWARE_MODE = 1 (parallel launch)
WALLETS_TO_WORK = 0             # 0 / 3 / 3, 20 / [3, 20]
SHUFFLE_WALLETS = False         # Shuffles wallets before launch
SHUFFLE_ROUTE = False           # Shuffles the route before launch
BREAK_ROUTE = False             # Stops route execution if an error occurs
SAVE_PROGRESS = False           # True or False | Enables saving account progress for Classic-routes
TELEGRAM_NOTIFICATIONS = False  # True or False | Enables Telegram notifications
WAIT_FOR_RECEIPT = False        # Wait for balance in the incoming network for LayerZero transactions

'------------------------------------------------SLEEP CONTROL---------------------------------------------------------'
SLEEP_MODE = False               # True or False | Enables sleep after each module and account
SLEEP_TIME = (10, 15)           # (min, max) seconds | Sleep time between modules.
SLEEP_TIME_STREAM = (5, 10)    # (min, max) seconds | Sleep time between accounts.

'-------------------------------------------------GAS CONTROL----------------------------------------------------------'
GAS_CONTROL = False              # True or False | Enables gas control
MAXIMUM_GWEI = 40               # Maximum GWEI for the software to work, can be changed during operation in maximum_gwei.json
SLEEP_TIME_GAS = 100            # Time until next gas check
CONTROL_TIMES_FOR_SLEEP = 5     # Number of checks
GAS_MULTIPLIER = 1.5            # Gas multiplier for transactions

'------------------------------------------------RETRY CONTROL---------------------------------------------------------'
MAXIMUM_RETRY = 3               # Number of retries on errors
SLEEP_TIME_RETRY = (5, 10)      # (min, max) seconds | Sleep time after each retry

'------------------------------------------------PROXY CONTROL---------------------------------------------------------'
USE_PROXY = False                # True or False | Enables proxy usage
MOBILE_PROXY = False             # True or False | Enables mobile proxy usage. USE_PROXY must be True
MOBILE_PROXY_URL_CHANGER = ['',
                            '',
                            '']  # ['link1', 'link2'..] | Links for IP change

'-----------------------------------------------SLIPPAGE CONTROL-------------------------------------------------------'
SLIPPAGE = 2                    # 0.54321 = 0.54321%, 1 = 1% | Slippage, by what % you are willing to receive less
PRICE_IMPACT = 3                # 0.54321 = 0.54321%, 1 = 1% | Maximum price impact for token swaps

'-----------------------------------------------APPROVE CONTROL--------------------------------------------------------'
UNLIMITED_APPROVE = False       # True or False Enables unlimited Approve for the contract

'------------------------------------------------SECURE DATA-----------------------------------------------------------'
# OKX API KEYS https://www.okx.com/account/my-api
OKX_API_KEY = ""
OKX_API_SECRET = ""
OKX_API_PASSPHRAS = ""

# EXCEL AND GOOGLE INFO
EXCEL_PASSWORD = False
EXCEL_PAGE_NAME = "EVM"

# TELEGRAM DATA
TG_TOKEN = ""  # https://t.me/BotFather
TG_ID = ""  # https://t.me/getmyid_bot

# 1INCH API KEY https://portal.1inch.dev/dashboard
ONEINCH_API_KEY = ""

# LAYERSWAP API KEY https://www.layerswap.io/dashboard
LAYERSWAP_API_KEY = ""
