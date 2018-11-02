from getpass import getpass
import os

def clear():
    os.system("clear")

""" INITIAL MENU """
def initialmenu():
    print('\n')
    print("*"*(len("welcome to terminal trader")+4))
    print("* WELCOME TO TERMINAL TRADER *")
    print("*"*(len("welcome to terminal trader")+4))
    print('\n')
    print("Main Menu")
    print("-"*len("Main Menu"))
    print("1. Create account")
    print("2. Log in")
    print("3. Quit")
    print('\n')

def initialmenu_choice():
    choice = input("Please make a selection: ").strip()
    return choice


""" CREATE ACCOUNT """
def create_username_prompt():
    print('\n')
    print("To return to main menu, type 'exit'")
    print("Please create a username:")

def create_username():    
    username = input()
    return username

def username_exists():
    print('\n')
    print("Username already exists. Try again")

def create_password_prompt():
    print("Create a unique password. Must be at least 8 characters long and contain at least one number")
    print("*input will be hidden for security*")

def create_password():
    password = getpass(prompt="")
    return password

def password_doublecheck_prompt():
    print("Please re-enter password:")

def password_doublecheck():
    password2 = getpass(prompt="")
    return password2

def short_password():
    print("Password must be 8 characters or longer. Try again")
    print('\n')

def password_nonum():
    print("Password must contain at least 1 number. Try again")
    print('\n')

def password_doublecheck_fail():
    print('\n')
    print("Passwords do not match. Try again")


""" LOG IN """
def enter_username_prompt():
    print('\n')
    print("To return to main menu, type 'exit'")
    print("Enter username:")

def enter_username():
    username = input()
    return username

def enter_password_prompt():
    print('\n')
    print("*input will be hidden for security*")
    print("Enter password:")

def enter_password():
    password = getpass(prompt="")
    return password

def login_success():
    print('\n')
    print("logging in...")
    print('\n')

def credentials_not_recognized():
    print("Password did not match or username does not exist")


""" LOG IN MENU """
def loginmenu(user):
    print('\n')
    print("Hello {}!".format(user.username))
    print('\n')
    print("Main Menu")
    print("-"*len("Main Menu"))
    print("1. View balance")
    print("2. Add funds")
    print("3. View portfolio")
    print("4. View transaction history")
    print("5. Check stock prices")
    print("6. Execute trade")
    print("7. Quit")
    print('\n')
    print("To return to main menu, type 'exit'")

def adminmenu(user):
    print('\n')
    print("Hello {}!".format(user.username))
    print('\n')
    print("Main Menu")
    print("-"*len("Main Menu"))
    print("1. View balance")
    print("2. Add funds")
    print("3. View portfolio")
    print("4. View transaction history")
    print("5. Check stock prices")
    print("6. Execute trade")
    print("7. View Accounts")
    print("8. Quit")
    print('\n')
    print("To return to main menu, type 'exit'")


def loginmenu_choice():
    choice = input("Please make a selection: ").strip()
    return choice
""" CHOICE 1 """
def showbalance(balance):
    print('\n')
    print("Your current balance is: {}".format(balance))
    print('\n')

def add_funds_ask():
    print("Would you like to add funds? (y/n):")

def add_funds_choice():
    choice = input().strip().lower()
    return choice
""" CHOICE 2 """
def increase_balance_prompt():
    print('\n')
    print("To return to main menu, type 'exit'")
    print("Enter amount to add:")

def increase_balance():
    amount = input().strip()
    return amount

def creditcard_prompt():
    print('\n')
    print("Please enter valid credit card number:")

def enter_creditcard():
    cardnumber = input().strip()
    return cardnumber

def invalid_creditcard():
    print('\n')
    print("Credit card is not valid. Try again")
    print('\n')

def deposit_accepted(balance):
    print('\n')
    print("Submitting deposit...")
    print('\n')
    print("Deposit accepted. Your new balance is ${}".format(balance))
    print('\n')
""" CHOICE 3 """
def showposition(position):
    print(position)
    print('\n')

def showpositions(positions):
    print('\n')
    for i in positions:
        print(i)
    print('\n')

def empty_portfolio():
    print('\n')
    print("Portfolio currently empty. Try buying some stock via the main menu!")
    print('\n')
""" CHOICE 4 """
def transaction_history_prompt():
    print('\n')
    print("Which would you like to see?")
    print("1. Transaction history for specific stock")
    print("2. Total transaction history")
    print('\n')
    print("To return to main menu, type 'exit'")

def choose_transaction_history():
    choice = input("Please make a selection: ").strip()
    return choice

def no_history(choice):
    print('\n')
    print("No trade history for {}".format(choice))
    print('\n')

def no_transaction_history():
    print('\n')
    print("No transaction history on this account")
    print('\n')

def show_transactions(transactions):
    print('\n')
    for i in transactions:
        print(i)
    print('\n')
""" CHOICE 5 """
def show_stock_price(ticker, price):
    print('\n')
    print("The current stock price of {} is ${}".format(ticker, price))
    print('\n')

def buy_sell_from_price_ask(ticker):
    print("Would you like to execute a trade for {}? (y/n):".format(ticker))

def buy_sell_from_price_choice():
    choice = input().strip().lower()
    return choice
""" CHOICE 6 """
def buy_or_sell_prompt():
    print('\n')
    print("Which would you like to do?")
    print('\n')
    print("1. Create a buy order")
    print("2. Create a sell order")
    print('\n')
    print("To return to the main menu, type 'exit'")
    print("Please make a selection:")

def buy_or_sell_choice():
    choice = input().strip()
    return choice

def buy_volume_prompt(ticker, price):
    print('\n')
    print("The current price of {} is ${}".format(ticker, price))
    print("How many shares of {} would you like to purchase?".format(ticker))

def buy_volume_ask():
    volume = input().strip()
    return volume

def insufficient_balance():
    print('\n')
    print("Order can't be executed: Insufficient funds")
    print('\n')

def execute_buy_prompt(price, volume):
    print('\n')
    print("Total purchase value = ${}".format(round((price*volume),2)))
    print("Trade ready to be executed, proceed? (y/n):")

def execute_trade():
    choice = input().strip().lower()
    return choice

def buy_success():
    print('\n')
    print("Posting order...")
    print('\n')
    print("Purchase successful!")
    print('\n')
    print("Here is your updated position:")

def position_doesnt_exist(ticker):
    print('\n')
    print("Position in {} no longer exists".format)

def stock_not_owned(ticker):
    print('\n')
    print("You currently don't own any shares of {}".format(ticker))
    print('\n')

def insufficient_amount_owned():
    print('\n')
    print("Trade can't be executed. Insufficient amount owned")
    print('\n')

def sell_volume_prompt(ticker, price):
    print('\n')
    print("The current price of {} is ${}".format(ticker, price))
    print("How many shares of {} would you like to sell?".format(ticker))

def sell_volume_ask():
    volume = input().strip()
    return volume

def execute_sell_prompt(price, volume):
    print('\n')
    print("Total sale value = ${}".format(round((price*volume),2)))
    print("Trade ready to be executed, proceed? (y/n):")

def sell_success():
    print('\n')
    print("Posting order...")
    print('\n')
    print("Sale successful!")
    print('\n')
    print("Here is your updated position:")

def position_closed():
    print('\n')
    print("Posting order...")
    print('\n')
    print("Sale successful!")
    print('\n')
    print("Position closed out")
    print('\n')

def trade_cancelled():
    print('\n')
    print("Execution cancelled. Transaction voided")
    print('\n')

def connection_error():
    print('\n')
    print("Connection timed out. Transaction cancelled")
    print('\n')

""" EXTRAS """
def stock_pick_prompt():
    print('\n')
    print("Please enter stock ticker:")

def stock_pick():
    choice = input().strip()
    return choice

def stock_doesnt_exist():
    print('\n')
    print("ERROR: Stock doesn't exist, ticker was incorrect, or connection timed out")
    print('\n')

def showaccounts(accounts):
    print('\n')
    for i in accounts:
        print(i)
    print('\n')


""" MISCELLANEOUS """
def wrongchoice():
    print('\n')
    print("That is not a valid selection")
    print('\n')

def return_ask():
    print("Would you like to return to the main menu? (y/n)")
    print("* 'n' will quit application *")

def returnchoice():
    choice = input().strip().lower()
    return choice

def goodbye():
    print('\n')
    print("Goodbye...")

