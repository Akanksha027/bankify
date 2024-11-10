class Account:
    def __init__(self, account_number, name, password, balance=0, transactions=None):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = transactions if transactions else []

    @classmethod
    def from_dict(cls, data):
        """Create an Account object from a dictionary."""
        return cls(
            account_number=data['account_number'],
            name=data['name'],
            password=data['password'],
            balance=data['balance'],
            transactions=data.get('transactions', [])
        )

    def to_dict(self):
        """Convert an Account object to a dictionary."""
        return {
            'account_number': self.account_number,
            'name': self.name,
            'password': self.password,
            'balance': self.balance,
            'transactions': self.transactions
        }

# In account.py

    def deposit(self, amount):
        """Deposit money into the account."""
        self.balance += amount
        # Log transaction with account details
        self.transactions.append(f"Deposited ${amount:.2f} (Account: {self.account_number})")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if self.balance >= amount:
            self.balance -= amount
            # Log transaction with account details
            self.transactions.append(f"Withdrew ${amount:.2f} (Account: {self.account_number})")
        else:
            print("Insufficient balance.")

    def transfer(self, to_account, amount):
        """Transfer money to another account."""
        if self.balance >= amount:
            self.balance -= amount
            to_account.balance += amount
            # Log transaction for sender
            self.transactions.append(f"Transferred ${amount:.2f} to {to_account.account_number} (Recipient: {to_account.name})")
            # Log transaction for receiver
            to_account.transactions.append(f"Received ${amount:.2f} from {self.account_number} (Sender: {self.name})")
        else:
            print("Insufficient balance.")