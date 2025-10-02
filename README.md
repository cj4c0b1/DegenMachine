
# 🚀 DegenMachine

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/chat-telegram-blue.svg)](https://t.me/askaer)

> **Warning**  
> By using DegenMachine, you accept all risks associated with DeFi operations, including but not limited to potential loss of assets, funds, or other valuables. Always test with small amounts first and use at your own risk.

## 📖 Overview

DegenMachine is a powerful DeFi automation tool designed for advanced users who need to interact with multiple blockchain networks. The tool provides a comprehensive suite of features for managing cross-chain operations, including swaps, bridges, and liquidity management.

### 🌟 Key Features

- **Multi-Chain Support**: Works with multiple EVM-compatible networks
- **Automated Operations**: Scriptable workflows for DeFi interactions
- **Gas Optimization**: Smart gas management with configurable limits
- **Modular Architecture**: Easy to extend with custom modules
- **Secure**: Non-custodial solution - your keys, your crypto

## 🛠 Installation

### Prerequisites

- Python 3.11+ (recommended)
- Git
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/cj4c0b1/DegenMachine.git
   cd DegenMachine
   ```

2. **Set up a virtual environment**
   ```bash
   # For Unix/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   
   # For Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your settings**
   - Copy `general_settings.py.example` to `general_settings.py`
   - Update the configuration with your wallet details and preferences

## 🚀 Quick Start

1. **Initialize the application**
   ```bash
   python main.py
   ```

2. **Follow the interactive menu** to select your desired operations

3. **For advanced usage**, check the available command-line options:
   ```bash
   python main.py --help
   ```

## 📂 Project Structure

```
DegenMachine/
├── data/                  # Data files and configurations
│   ├── logs/              # Application logs
│   └── services/          # Service configurations
├── modules/               # Core functionality modules
│   ├── bridges/           # Bridge implementations
│   ├── swaps/             # DEX swap modules
│   └── others/            # Additional utilities
├── utils/                 # Helper utilities
│   └── stark_signature/   # StarkNet signature utilities
├── .gitignore            # Git ignore rules
├── CHANGELOG.md          # Project changelog
├── config.py             # Main configuration
├── main.py               # Entry point
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## ⚙️ Configuration

Edit `general_settings.py` to configure:
- Network settings
- Wallet configurations
- Gas parameters
- Slippage tolerance
- And more...

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❓ Support

For support and questions:

- Join our [Telegram Channel](https://t.me/askaer) for updates
- Open an [Issue](https://github.com/cj4c0b1/DegenMachine/issues) for bugs or feature requests
- [@askaer](https://t.me/realaskaer) for critical issues (Telegram)

## ❤️ Donations

Support the development of DegenMachine:

- **Original Developer (Askaer)**: 
  ```
  0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5
  ```
- **Maintainer (j4c0b1)**: 
  ```
  0x7B267EcEc11a07CA2a782E4b8a51558a70449e7c
  ```

## 📜 Credits

- **Original Developer**: [Askaer](https://t.me/askaer)
- **Maintainer**: [j4c0b1](https://github.com/cj4c0b1)

## 🔒 Security

Please report any security issues to the maintainers directly. For critical security issues, please use the PGP key available in the repository.
