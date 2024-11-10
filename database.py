import json
from account import Account  # Import the Account class from account.py

def load_accounts():
    """Load accounts from a JSON file."""
    try:
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            # Create Account objects from the data in the JSON file
            return {acc_num: Account.from_dict(acc) for acc_num, acc in data.items()}
    except FileNotFoundError:
        # Return an empty dictionary if the file doesn't exist
        return {}

def save_accounts(accounts):
    """Save accounts to a JSON file."""
    with open('accounts.json', 'w') as f:
        # Convert Account objects to dictionaries and save them to the JSON file
        data = {acc.account_number: acc.to_dict() for acc in accounts.values()}
        json.dump(data, f, indent=4)
