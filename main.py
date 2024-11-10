import tkinter as tk
from tkinter import ttk, messagebox
from account import Account
from database import load_accounts, save_accounts

# Load accounts
accounts = load_accounts()
current_account = None

# Colors and Styles
PRIMARY_COLOR = "#4a90e2"
SECONDARY_COLOR = "#d9e6f2"
FONT = ("Arial", 12)

# Initialize main login window
login_window = tk.Tk()
login_window.title("Professional Banking System")
login_window.geometry("400x300")
login_window.config(bg=SECONDARY_COLOR)

# Header
header = tk.Label(login_window, text="Welcome to Your Banking System", font=("Arial", 16, "bold"), bg=PRIMARY_COLOR, fg="white")
header.pack(pady=10, fill="x")

# Login Frame
login_frame = tk.Frame(login_window, bg=SECONDARY_COLOR, padx=10, pady=10)
login_frame.pack(pady=10)

account_number_label = tk.Label(login_frame, text="Account Number:", bg=SECONDARY_COLOR, font=FONT)
account_number_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
account_number_entry = tk.Entry(login_frame, font=FONT)
account_number_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(login_frame, text="Password:", bg=SECONDARY_COLOR, font=FONT)
password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
password_entry = tk.Entry(login_frame, show="*", font=FONT)
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Login function
def login():
    global current_account
    account_number = account_number_entry.get()
    password = password_entry.get()
    account = accounts.get(account_number)
    if account and account.password == password:
        current_account = account
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid account number or password")

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2, pady=10)

# Registration function
def register():
    register_window = tk.Toplevel()
    register_window.title("Register New Account")
    register_window.geometry("350x300")
    register_window.config(bg=SECONDARY_COLOR)

    tk.Label(register_window, text="Create a New Account", font=("Arial", 14, "bold"), bg=SECONDARY_COLOR).pack(pady=10)

    tk.Label(register_window, text="Account Number:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    acc_num_entry = tk.Entry(register_window, font=FONT)
    acc_num_entry.pack(pady=5)

    tk.Label(register_window, text="Name:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    name_entry = tk.Entry(register_window, font=FONT)
    name_entry.pack(pady=5)

    tk.Label(register_window, text="Password:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    pass_entry = tk.Entry(register_window, show="*", font=FONT)
    pass_entry.pack(pady=5)

    tk.Label(register_window, text="Initial Deposit:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    deposit_entry = tk.Entry(register_window, font=FONT)
    deposit_entry.pack(pady=5)

    def create_account():
        account_number = acc_num_entry.get()
        name = name_entry.get()
        password = pass_entry.get()
        try:
            initial_deposit = float(deposit_entry.get())
            if account_number not in accounts:
                accounts[account_number] = Account(account_number, name, password, initial_deposit)
                save_accounts(accounts)
                messagebox.showinfo("Registration Successful", "Account created successfully!")
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Account number already exists.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid deposit amount.")

    ttk.Button(register_window, text="Submit", command=create_account).pack(pady=10)

# Register button on the login screen
register_button = ttk.Button(login_window, text="Register New Account", command=register)
register_button.pack(pady=5)

# Dashboard function
def open_dashboard():
    login_window.withdraw()
    dashboard = tk.Toplevel()
    dashboard.title("Dashboard")
    dashboard.geometry("400x400")
    dashboard.config(bg=SECONDARY_COLOR)

    tk.Label(dashboard, text=f"Welcome, {current_account.name}!", font=("Arial", 16, "bold"), bg=PRIMARY_COLOR, fg="white").pack(fill="x", pady=10)

    balance_label = tk.Label(dashboard, text=f"Current Balance: ${current_account.balance:.2f}", font=("Arial", 14), bg=SECONDARY_COLOR)
    balance_label.pack(pady=10)

    ttk.Button(dashboard, text="Deposit", command=lambda: perform_transaction("deposit", balance_label)).pack(pady=5)
    ttk.Button(dashboard, text="Withdraw", command=lambda: perform_transaction("withdraw", balance_label)).pack(pady=5)
    ttk.Button(dashboard, text="Transfer Funds", command=lambda: transfer_funds(balance_label)).pack(pady=5)
    ttk.Button(dashboard, text="View Profile", command=view_profile).pack(pady=5)  # New: Button for Profile Page
    ttk.Button(dashboard, text="Logout", command=lambda: logout(dashboard)).pack(pady=10)


# In main.py

# In main.py, view_profile function
def view_profile():
    profile_window = tk.Toplevel()
    profile_window.title("User Profile")
    profile_window.geometry("400x400")
    profile_window.config(bg=SECONDARY_COLOR)

    tk.Label(profile_window, text=f"User Profile: {current_account.name}", font=("Arial", 16, "bold"), bg=PRIMARY_COLOR, fg="white").pack(fill="x", pady=10)
    tk.Label(profile_window, text=f"Account Number: {current_account.account_number}", font=FONT, bg=SECONDARY_COLOR).pack(pady=5)
    tk.Label(profile_window, text=f"Current Balance: ${current_account.balance:.2f}", font=FONT, bg=SECONDARY_COLOR).pack(pady=5)

    tk.Label(profile_window, text="Transaction History:", font=("Arial", 14, "bold"), bg=SECONDARY_COLOR).pack(pady=10)

    transaction_frame = tk.Frame(profile_window, bg=SECONDARY_COLOR)
    transaction_frame.pack(pady=5)

    # Display each transaction
    for transaction in current_account.transactions:
        tk.Label(transaction_frame, text=transaction, font=("Arial", 10), bg=SECONDARY_COLOR).pack(anchor="w")

# Transaction function
def perform_transaction(transaction_type, balance_label):
    transaction_window = tk.Toplevel()
    transaction_window.title(f"{transaction_type.capitalize()} Funds")
    transaction_window.geometry("300x200")
    transaction_window.config(bg=SECONDARY_COLOR)

    tk.Label(transaction_window, text=f"Enter amount to {transaction_type}:", bg=SECONDARY_COLOR, font=FONT).pack(pady=10)
    amount_entry = tk.Entry(transaction_window, font=FONT)
    amount_entry.pack(pady=5)

    def process_transaction():
        try:
            amount = float(amount_entry.get())
            if transaction_type == "deposit":
                current_account.deposit(amount)
            elif transaction_type == "withdraw":
                current_account.withdraw(amount)
            save_accounts(accounts)
            balance_label.config(text=f"Current Balance: ${current_account.balance:.2f}")
            transaction_window.destroy()
            messagebox.showinfo("Success", f"{transaction_type.capitalize()} completed.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    ttk.Button(transaction_window, text="Submit", command=process_transaction).pack(pady=10)

# Transfer funds function
def transfer_funds(balance_label):
    transfer_window = tk.Toplevel()
    transfer_window.title("Transfer Funds")
    transfer_window.geometry("300x200")
    transfer_window.config(bg=SECONDARY_COLOR)

    tk.Label(transfer_window, text="Recipient Account Number:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    account_entry = tk.Entry(transfer_window, font=FONT)
    account_entry.pack(pady=5)

    tk.Label(transfer_window, text="Amount to Transfer:", bg=SECONDARY_COLOR, font=FONT).pack(pady=5)
    amount_entry = tk.Entry(transfer_window, font=FONT)
    amount_entry.pack(pady=5)

    def process_transfer():
        try:
            to_account_number = account_entry.get()
            amount = float(amount_entry.get())
            to_account = accounts.get(to_account_number)
            if to_account and amount <= current_account.balance:
                current_account.withdraw(amount)
                to_account.deposit(amount)
                save_accounts(accounts)
                balance_label.config(text=f"Current Balance: ${current_account.balance:.2f}")
                transfer_window.destroy()
                messagebox.showinfo("Transfer Success", "Funds transferred successfully.")
            else:
                messagebox.showerror("Transfer Failed", "Invalid details or insufficient funds.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid details.")

    ttk.Button(transfer_window, text="Submit", command=process_transfer).pack(pady=10)

# Logout function
def logout(dashboard):
    global current_account
    current_account = None
    dashboard.destroy()
    login_window.deiconify()

login_window.mainloop()
