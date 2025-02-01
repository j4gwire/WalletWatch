import requests

# Banner
def print_intro():
    print("Welcome to WalletWatch!")
    print("Fetch wallet transaction details with Blockchain API and display wallet information.\n")

def fetch_wallet_data(wallet):
    """ Fetch wallet data from the Blockchain API """
    url = f"https://blockchain.info/rawaddr/{wallet}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an error for non-2xx HTTP responses
        
        data = response.json()
        if 'error' in data:
            print(f"[-] Error: {data['error']}")
            return None  # Return None if an error in the API response
        
        return data  # Return data if no error
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Network error while accessing the wallet {wallet}: {e}")
    except Exception as e:
        print(f"[-] Unexpected error while processing the wallet {wallet}: {e}")
    
    return None  # Return None if something goes wrong

def extract_wallet_info(data):
    """ Extract necessary information from the API response """
    if not data:
        return 'N/A', 'N/A', 'N/A', 'N/A'
    
    transactions = data.get('n_tx', 'N/A')
    total_received = data.get('total_received', 'N/A') / 1e8  # Convert satoshis to BTC
    total_sent = data.get('total_sent', 'N/A') / 1e8  # Convert satoshis to BTC
    balance = data.get('final_balance', 'N/A') / 1e8  # Convert satoshis to BTC
    
    return transactions, total_received, total_sent, balance

def display_wallet_info(wallet, transactions, total_received, total_sent, balance):
    """ Display wallet data in plain text format """
    print(f"\nWallet Address: {wallet}")
    print(f"Transactions: {transactions}")
    print(f"Total Received: {total_received:.8f} BTC")
    print(f"Total Sent: {total_sent:.8f} BTC")
    print(f"Balance: {balance:.8f} BTC")

def get_wallet_address():
    """ Get a valid wallet address from the user input """
    while True:
        wallet = input("Enter wallet address: ").strip()
        if wallet:
            return wallet
        else:
            print("[-] Invalid wallet address. Please try again.")

def search_another_wallet():
    """ Ask the user if they want to search for another wallet """
    while True:
        response = input("\nWould you like to search for another wallet? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        else:
            print("[-] Invalid input. Please enter 'y' or 'n'.")

# Main Execution
print_intro()  # Introduction message

while True:
    wallet = get_wallet_address()  # Get wallet address from user input

    # Fetch wallet data from the Blockchain API
    wallet_data = fetch_wallet_data(wallet)

    # Extract relevant information if data is valid
    transactions, total_received, total_sent, balance = extract_wallet_info(wallet_data)

    # Display the results
    display_wallet_info(wallet, transactions, total_received, total_sent, balance)

    # Ask the user if they want to search for another wallet
    if not search_another_wallet():
        print("\n[+] Goodbye!")
        break
