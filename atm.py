
# account number, account name, amount
# set up or create account
# print account details
# make deposit or withdrawal
import random


class AccountOwner:
    def __init__(self, accountName, accountNumber, balance=0):
        self.accountName = accountName
        self.accountNumber = accountNumber
        self.balance = balance

    def __str__(self):
        return f"Account Name: {self.accountName}, Account Number: {self.accountNumber}, Balance: {self.balance}"

    def deposit(self, amount):
        if amount <= 0:
            print("You cannot deposit amount less than or equals 0")
        else:
            self.balance += amount

    def withdrawal(self, amount):
        if amount <= 0:
            print("Please you cannot withdraw amount less than 0")
        elif amount >= self.balance:
            print(f"Insufficient balance: current Balance: GHS {self.balance}")
        else:
            self.balance -= amount

# OPEN BANK


def generate_account_number():
    account = [random.randint(1, 9) for _ in range(10)] # get 10 random numbers
    account_str = [str(acc) for acc in account] # convert the numbers to string
    return "".join(account_str) # join the numbers to a single string number


def account_setup():
    accountName = input("Please enter your name: ")
    starting_deposit = int(input("Enter starting deposit: GHS "))
    account = generate_account_number()
    return accountName, starting_deposit, account


def main():
    flag: bool = False
    name, starting_deposit, account_number = account_setup()
    # print(f"Name: {name}, Starting Deposit: {starting_deposit}, account: {account_number}")
    account = AccountOwner(name, account_number, starting_deposit)
    operation = int(input("\nWelcome, Please Select your operation\n 1. Print Account Details \n 2. Make Deposit  \n 3. Withdrawal \n Enter Option: "))
    set_operation(operation, account)


def set_operation(operation: int, account: 'AccountOwner'):
    if operation == 1:
        print(account)
    elif operation == 2:
        amount = int(input("Enter Deposit Amount GHS: "))
        account.deposit(amount)
    elif operation == 3:
        amount = int(input("Enter Withdrawal Amount GHS: "))
        account.withdrawal(amount)
    main()



main()


# print(account_setup())

# print(generate_account_number())


# Wisdom = AccountOwner("Godzo Wisdom", "36563637637328", 0)
# print(Wisdom)
#
# Wisdom.deposit(100)
# Wisdom.deposit(50)
# Wisdom.deposit(5)
#
# print(Wisdom)
#
# Wisdom.withdrawal(0)
# print(Wisdom)


# for fruit in fruits:
#     print(fruit)
