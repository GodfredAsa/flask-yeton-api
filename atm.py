#
# # account number, account name, amount
# # set up or create account
# # print account details
# # make deposit or withdrawal
# import random
#
#
# class AccountOwner:
#     def __init__(self, accountName, accountNumber, balance=0):
#         self.accountName = accountName
#         self.accountNumber = accountNumber
#         self.balance = balance
#
#     def __str__(self):
#         return f"Account Name: {self.accountName}, Account Number: {self.accountNumber}, Balance: {self.balance}"
#
#     def deposit(self, amount):
#         if amount <= 0:
#             print("You cannot deposit amount less than or equals 0")
#         else:
#             self.balance += amount
#
#     def withdrawal(self, amount):
#         if amount <= 0:
#             print("Please you cannot withdraw amount less than 0")
#         elif amount >= self.balance:
#             print(f"Insufficient balance: current Balance: GHS {self.balance}")
#         else:
#             self.balance -= amount
#
# # OPEN BANK
#
#
# def generate_account_number():
#     account = [random.randint(1, 9) for _ in range(10)] # get 10 random numbers
#     account_str = [str(acc) for acc in account] # convert the numbers to string
#     return "".join(account_str) # join the numbers to a single string number
#
#
# def account_setup():
#     accountName = input("Please enter your name: ")
#     starting_deposit = int(input("Enter starting deposit: GHS "))
#     account = generate_account_number()
#     return accountName, starting_deposit, account
#
#
# def main():
#     flag: bool = False
#     name, starting_deposit, account_number = account_setup()
#     # print(f"Name: {name}, Starting Deposit: {starting_deposit}, account: {account_number}")
#     account = AccountOwner(name, account_number, starting_deposit)
#     operation = int(input("\nWelcome, Please Select your operation\n 1. Print Account Details \n 2. Make Deposit  \n 3. Withdrawal \n Enter Option: "))
#     set_operation(operation, account)
#
#
# def set_operation(operation: int, account: 'AccountOwner'):
#     if operation == 1:
#         print(account)
#     elif operation == 2:
#         amount = int(input("Enter Deposit Amount GHS: "))
#         account.deposit(amount)
#     elif operation == 3:
#         amount = int(input("Enter Withdrawal Amount GHS: "))
#         account.withdrawal(amount)
#     main()



# main()


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


import json
from collections import defaultdict

# Sample JSON data
data = [
    {
        "orderId": "0bd42dc8-3657-44ec-939c-5e97b09b4d70",
        "price": 10.0,
        "quantity": 1,
        "totalCost": 8.0,
        "item": "X-YOU",
        "user": "0550026240",
        "profit": 2.0,
        "orderStatus": "COMPLETED",
        "paymentStatus": "PAID",
        "orderDate": "2024-12-28",
        "updatedDate": "2024-12-28 17:23:22.720918",
        "orderCode": "SW65Q01"
    },
    {
        "orderId": "a2d42dc8-1234-44ec-939c-5e97b09b4d71",
        "price": 15.0,
        "quantity": 2,
        "totalCost": 30.0,
        "item": "Y-ZONE",
        "user": "0550026241",
        "profit": 5.0,
        "orderStatus": "COMPLETED",
        "paymentStatus": "PAID",
        "orderDate": "2024-12-27",
        "updatedDate": "2024-12-27 12:15:10.720918",
        "orderCode": "SW65Q02"
    },
    {
        "orderId": "c3f52ec8-5678-44ec-939c-5e97b09b4d72",
        "price": 20.0,
        "quantity": 1,
        "totalCost": 20.0,
        "item": "Z-PRO",
        "user": "0550026242",
        "profit": 8.0,
        "orderStatus": "COMPLETED",
        "paymentStatus": "PAID",
        "orderDate": "2024-12-26",
        "updatedDate": "2024-12-26 15:45:33.720918",
        "orderCode": "SW65Q03"
    },
    {
        "orderId": "d4g62fc8-9876-44ec-939c-5e97b09b4d73",
        "price": 25.0,
        "quantity": 3,
        "totalCost": 75.0,
        "item": "W-MAX",
        "user": "0550026243",
        "profit": 15.0,
        "orderStatus": "COMPLETED",
        "paymentStatus": "PAID",
        "orderDate": "2024-12-25",
        "updatedDate": "2024-12-25 10:30:55.720918",
        "orderCode": "SW65Q04"
    },
    {
        "orderId": "e5h72gc8-6543-44ec-939c-5e97b09b4d74",
        "price": 12.0,
        "quantity": 2,
        "totalCost": 24.0,
        "item": "V-PLUS",
        "user": "0550026244",
        "profit": 6.0,
        "orderStatus": "COMPLETED",
        "paymentStatus": "PAID",
        "orderDate": "2024-12-24",
        "updatedDate": "2024-12-24 08:20:44.720918",
        "orderCode": "SW65Q05"
    }
]



def calculate_sales_per_day(data):
    # Group sales by orderDate
    sales_per_day = defaultdict(float)
    for order in data:
        order_date = order["orderDate"]
        total_cost = order["totalCost"]
        sales_per_day[order_date] += total_cost

    return dict(sales_per_day)


# Calculate and print sales per day
sales_per_day = calculate_sales_per_day(data)
print("Sales Per Day:")
for date, total_sales in sales_per_day.items():
    print(f"{date}: ${total_sales:.2f}")
