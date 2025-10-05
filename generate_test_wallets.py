import os
import json
from eth_account import Account
from web3 import Web3
import pandas as pd
from getpass import getpass
from msoffcrypto import OfficeFile
import io

def generate_wallets(count=5):
    wallets = []
    for i in range(1, count + 1):
        # Create a new account
        account = Account.create()
        private_key = account._private_key.hex()
        address = account.address
        
        # Add to wallets list
        wallets.append({
            'private_key': private_key,
            'name': f'test_wallet_{i}',
            'address': address
        })
        print(f"Generated wallet {i}: {address}")
    
    return wallets

def save_to_excel(wallets, filename='data/accounts_data.xlsx', password=None):
    # Create DataFrame
    df = pd.DataFrame(wallets)
    
    # Save to Excel
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if password:
        # Save with password protection
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Wallets')
        
        # Encrypt the file
        with open(filename, 'rb') as file:
            src = io.BytesIO(file.read())
        
        office_file = OfficeFile(src)
        office_file.load_key(password=password)
        
        with open(filename, 'wb') as file:
            office_file.decrypt(file)
        
        print(f"\n✅ Wallets saved to {filename} with password protection")
    else:
        df.to_excel(filename, index=False)
        print(f"\n✅ Wallets saved to {filename} (no password)")

if __name__ == "__main__":
    print("🚀 DegenMachine Test Wallet Generator")
    print("-----------------------------------\n")
    
    # Get number of wallets to generate
    try:
        count = int(input("How many test wallets would you like to generate? (default: 5) ") or "5")
        if count < 1:
            raise ValueError("Please enter a number greater than 0")
    except ValueError as e:
        print(f"Invalid input: {e}. Using default value of 5.")
        count = 5
    
    # Generate wallets
    print(f"\nGenerating {count} test wallets...")
    wallets = generate_wallets(count)
    
    # Ask about password protection
    use_password = input("\nWould you like to password protect the Excel file? (y/n, default: y) ").lower() != 'n'
    password = None
    
    if use_password:
        while True:
            password = getpass("Enter password for Excel file (min 8 characters): ")
            if len(password) >= 8:
                confirm = getpass("Confirm password: ")
                if password == confirm:
                    break
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Password must be at least 8 characters long.")
    
    # Save to Excel
    try:
        save_to_excel(wallets, password=password)
        
        print("\n🔐 Important Security Information:")
        print("1. Keep this file secure and never share it")
        print("2. The private keys are only shown here once")
        print("3. For testing, you can fund these wallets with testnet ETH")
        print("\nGenerated Wallets:")
        for wallet in wallets:
            print(f"\nWallet: {wallet['name']}")
            print(f"Address: {wallet['address']}")
            print(f"Private Key: {wallet['private_key']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nGenerated Wallets (save this information):")
        for wallet in wallets:
            print(f"\nWallet: {wallet['name']}")
            print(f"Address: {wallet['address']}")
            print(f"Private Key: {wallet['private_key']}")
            print("-" * 40)
