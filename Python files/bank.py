import json
import os
import random

DATA_FILE = 'bank_data.json'

class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposit of ₦{amount:.2f} was successful. New balance: ₦{self.balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Withdrew ₦{amount:.2f}. New balance: ₦{self.balance:.2f}")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance
        
    def to_dict(self):
        return {
            'type': 'BankAccount',
            'account_number': self.account_number,
            'account_holder': self.account_holder,
            'balance': self.balance
        }

class SavingsAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0.0):
        super().__init__(account_number, account_holder, balance)
        self.min_balance = 1000.0

    def withdraw(self, amount):
        if amount > 0:
            if (self.balance - amount) >= self.min_balance:
                self.balance -= amount
                print(f"Withdrew ₦{amount:.2f}. New balance: ₦{self.balance:.2f}")
            else:
                print(f"Transaction Blocked! Withdrawal of ₦{amount:.2f} drops balance below the ₦{self.min_balance:.2f} minimum.")
        else:
            print("Withdrawal amount must be positive.")

    def add_interest(self, rate):
        if rate > 0:
            interest_amount = self.balance * (rate / 100)
            self.balance += interest_amount
            print(f"Added {rate}% interest (₦{interest_amount:.2f}). New balance: ₦{self.balance:.2f}")
        else:
            print("Interest rate must be positive.")
            
    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'SavingsAccount'
        return data

class CurrentAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0.0, overdraft_limit=50000.0):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = float(overdraft_limit)

    def withdraw(self, amount):
        if amount > 0:
            if (self.balance - amount) >= -self.overdraft_limit:
                self.balance -= amount
                print(f"Withdrew ₦{amount:.2f}. New balance: ₦{self.balance:.2f}")
            else:
                print(f"Transaction Blocked! Withdrawal exceeds the overdraft limit of ₦{self.overdraft_limit:.2f}.")
        else:
            print("Withdrawal amount must be positive.")
            
    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'CurrentAccount'
        data['overdraft_limit'] = self.overdraft_limit
        return data


def save_data(accounts_dict):
    data_to_save = [acc.to_dict() for acc in accounts_dict.values()]
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    accounts_dict = {}
    if not os.path.exists(DATA_FILE):
        return accounts_dict
        
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
        for acc_data in data:
            acc_type = acc_data.get('type')
            acc_num = acc_data['account_number']
            acc_holder = acc_data['account_holder']
            balance = acc_data['balance']
            
            if acc_type == 'SavingsAccount':
                accounts_dict[acc_num] = SavingsAccount(acc_num, acc_holder, balance)
            elif acc_type == 'CurrentAccount':
                overdraft_limit = acc_data.get('overdraft_limit', 50000.0)
                accounts_dict[acc_num] = CurrentAccount(acc_num, acc_holder, balance, overdraft_limit)
            else:
                accounts_dict[acc_num] = BankAccount(acc_num, acc_holder, balance)
    except Exception as e:
        print(f"Error loading data: {e}")
        
    return accounts_dict

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def main():
    accounts = load_data()
    
    while True:
        print("\n--- Core Banking System Simulator ---")
        print("1. Open New Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit (Saves Data)")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter account holder's name: ")
            acc_type = input("Choose account type (1 for Savings, 2 for Current): ")
            try:
                initial_deposit = float(input("Enter initial deposit amount: "))
            except ValueError:
                print("Invalid amount. Account creation aborted.")
                continue
            
            acc_num = generate_account_number()
            while acc_num in accounts:
                acc_num = generate_account_number()
                
            if acc_type == '1':
                accounts[acc_num] = SavingsAccount(acc_num, name, initial_deposit)
                print(f"Savings Account created successfully! Account Number: {acc_num}")
            elif acc_type == '2':
                overdraft_input = input("Enter overdraft limit (or press Enter for default 50000): ")
                try:
                    overdraft = float(overdraft_input) if overdraft_input else 50000.0
                except ValueError:
                    print("Invalid amount. Using default 50000.")
                    overdraft = 50000.0
                accounts[acc_num] = CurrentAccount(acc_num, name, initial_deposit, overdraft)
                print(f"Current Account created successfully! Account Number: {acc_num}")
            else:
                print("Invalid account type.")
                
        elif choice == '2':
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                try:
                    amount = float(input("Enter amount to deposit: "))
                    accounts[acc_num].deposit(amount)
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Account not found.")
                
        elif choice == '3':
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    accounts[acc_num].withdraw(amount)
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Account not found.")
                
        elif choice == '4':
            acc_num = input("Enter account number: ")
            if acc_num in accounts:
                print(f"Current balance for account {acc_num} ({accounts[acc_num].account_holder}): ₦{accounts[acc_num].get_balance():.2f}")
            else:
                print("Account not found.")
                
        elif choice == '5':
            save_data(accounts)
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()