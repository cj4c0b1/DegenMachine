# DegenMachine - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Configuration Guide](#configuration-guide)
4. [Wallet Management](#wallet-management)
5. [Bridge Operations](#bridge-operations)
6. [OKX Integration](#okx-integration)
7. [Running the Software](#running-the-software)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)

## Introduction

DegenMachine is a powerful DeFi automation tool designed for managing cross-chain operations. This guide will help you set up and use the software effectively.

## Quick Start

1. **Prerequisites**
   - Python 3.11+
   - Git
   - Web3 wallet with test funds

2. **Installation**
   ```bash
   git clone https://github.com/cj4c0b1/DegenMachine.git
   cd DegenMachine
   python3.11 -m venv .venv311
   source .venv311/bin/activate  # On Windows: .venv311\Scripts\activate
   pip install -r requirements.txt
   ```

## Configuration Guide

### General Settings (`general_settings.py`)

| Setting | Description | Example |
|---------|-------------|---------|
| `GLOBAL_NETWORK` | Default network for operations | `9` (Starknet) |
| `SOFTWARE_MODE` | `0` for sequential, `1` for parallel execution | `0` |
| `TELEGRAM_NOTIFICATIONS` | Enable/disable Telegram alerts | `False` |
| `SAVE_PROGRESS` | Save progress between runs | `True` |
| `BREAK_ROUTE` | Stop execution on first error | `True` (recommended for testing) |

### Network IDs

| Network | ID |
|---------|----|
| Arbitrum | 1 |
| zkSync Era | 11 |
| Starknet | 9 |
| Polygon | 6 |
| Optimism | 7 |
| Base | 3 |
| ZKFair | 45 |

## Wallet Management

1. **Adding Wallets**
   Edit `config.py` to add your wallets:
   ```python
   ACCOUNT_NAMES = ["MyWallet1", "MyWallet2"]
   PRIVATE_KEYS = ["0x...", "0x..."]
   PROXIES = [None, "http://user:pass@ip:port"]  # Optional
   ```

2. **Proxy Setup**
   - Set `USE_PROXY = True` in `general_settings.py` if using proxies
   - Format: `http://username:password@ip:port`

## Bridge Operations

### Supported Bridges
1. **Orbiter Finance**
   - Configure in `settings.py`:
   ```python
   ORBITER_CHAIN_ID_FROM = [7]  # Source network (Arbitrum)
   ORBITER_CHAIN_ID_TO = [45]   # Destination (ZKFair)
   ORBITER_DEPOSIT_AMOUNT = (0.001, 0.001)  # Min, Max in ETH
   ORBITER_TOKEN_NAME = 'ETH'  # or 'USDC'
   ```

2. **LayerSwap**
   - Requires API key
   ```python
   LAYERSWAP_API_KEY = "your_api_key"
   LAYERSWAP_CHAIN_ID_FROM = [1]
   LAYERSWAP_CHAIN_ID_TO = [4]
   LAYERSWAP_DEPOSIT_AMOUNT = (0.002, 0.002)
   ```

## OKX Integration

1. **Withdrawal Settings**
   ```python
   OKX_WITHDRAW_NETWORK = 22  # Polygon
   OKX_WITHDRAW_AMOUNT = (1, 1)  # Min, Max
   ```

2. **Deposit Settings**
   ```python
   OKX_DEPOSIT_NETWORK = 32  # USDC-Polygon
   OKX_DEPOSIT_AMOUNT = ('100', '100')  # Min, Max
   ```

## Running the Software

1. **Basic Usage**
   ```bash
   python main.py
   ```
   - Select options from the interactive menu

2. **Common Operations**
   - `🚀 Start running classic routes` - Execute configured routes
   - `📄 Generate classic-route` - Create new route files
   - `💾 Create OKX withdrawal file` - Generate OKX withdrawal config
   - `✅ Check proxy connections` - Verify proxy status

## Troubleshooting

### Common Issues
1. **Module Not Found**
   ```
   Ensure you've activated the virtual environment and installed requirements:
   source .venv311/bin/activate
   pip install -r requirements.txt
   ```

2. **Insufficient Funds**
   - Check wallet balances
   - Verify network RPC endpoints
   - Adjust gas settings if needed

3. **Proxy Connection Issues**
   - Verify proxy format: `http://user:pass@ip:port`
   - Test proxy with `Check proxy connections`

## Security Best Practices

1. **Never share private keys**
   - Use environment variables for sensitive data
   - Consider using a hardware wallet for large amounts

2. **Test with Small Amounts**
   - Always test with minimal amounts first
   - Verify transactions on block explorers

3. **Regular Updates**
   - Keep the software updated
   - Monitor for security announcements

## Support

For additional help:
- [Telegram Support](https://t.me/askaer)
- [GitHub Issues](https://github.com/cj4c0b1/DegenMachine/issues)

---
*Last Updated: October 2023*
