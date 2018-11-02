import view
import model

def initialmenu():
    view.initialmenu()
    choice = view.initialmenu_choice()
    while choice not in ["1", "2", "3"]:
        view.wrongchoice()
        view.initialmenu()
        choice = view.initialmenu_choice()
    if choice == "1":
        create_account()
    if choice == "2":
        login()
    if choice == "3":
        view.goodbye()
        quit()

def create_account():
    view.create_username_prompt()
    username = view.create_username()
    if username == "exit":
        return initialmenu()
    u = model.Account(username=username)
    while not u.username_exists_check(username):
        view.username_exists()
        view.create_username_prompt()
        username = view.create_username()
        if username == "exit":
            return initialmenu()
        u=model.Account(username=username)
    view.create_password_prompt()
    password = view.create_password()
    if password == 'exit':
        return initialmenu()
    password_check = model.password_check(password)
    while password_check == "1":
        view.short_password()
        view.create_password_prompt()
        password = view.create_password()
        password_check = model.password_check(password)
    while password_check == "2":
        view.password_nonum()
        view.create_password_prompt()
        password = view.create_password()
        password_check = model.password_check(password)
    view.password_doublecheck_prompt()
    password2 = view.password_doublecheck()
    if password2 == 'exit':
        return initialmenu()
    while password2 != password:
        view.password_doublecheck_fail()
        return create_account()
    u.set_pass_hash(password)
    u.balance = 0.00
    u.save()
    return loginmenu(u)

def login():
    view.enter_username_prompt()
    username = view.enter_username()
    if username == 'exit':
        return initialmenu()
    view.enter_password_prompt()
    password = view.enter_password()
    u = model.Account()
    while not u.set_from_credentials(username, password):
        view.credentials_not_recognized()
        view.enter_username_prompt()
        username = view.enter_username()
        if username == 'exit':
            return initialmenu()
        view.enter_password_prompt()
        password = view.enter_password()
    u.set_from_credentials(username, password)
    view.login_success()
    return loginmenu(u)

def loginmenu(user):
    if user.acct_type == "ADMN":
        view.adminmenu(user)
        choice = view.loginmenu_choice()
        while choice not in ["exit", "1", "2", "3", "4", "5", "6", "7", "8"]:
            view.wrongchoice()
            choice = view.loginmenu_choice()
        if choice == "exit":
            initialmenu()
        if choice == "1":
            viewbalance(user)
        if choice == "2":
            addfunds(user)
        if choice == "3":
            viewportfolio(user)
        if choice == "4":
            viewtransactions(user)
        if choice == "5":
            stockprices(user)
        if choice == "6":
            executetrade(user)
        if choice == "7":
            adminaccountviewer(user)
        if choice == "8":
            exit()
    view.loginmenu(user)
    choice = view.loginmenu_choice()
    while choice not in ["exit", "1", "2", "3", "4", "5", "6", "7"]:
        view.wrongchoice()
        choice = view.loginmenu_choice()
    if choice == "exit":
        initialmenu()
    if choice == "1":
        viewbalance(user)
    if choice == "2":
        addfunds(user)
    if choice == "3":
        viewportfolio(user)
    if choice == "4":
        viewtransactions(user)
    if choice == "5":
        stockprices(user)
    if choice == "6":
        executetrade(user)
    if choice == "7":
        exit()

def viewbalance(user):
    balance = user.getbalance()
    view.showbalance(balance)
    view.add_funds_ask()
    choice = view.add_funds_choice()
    while choice not in ["y","n"]:
        view.wrongchoice()
        view.add_funds_ask()
        choice = view.add_funds_choice()
    if choice == "y":
        return addfunds(user)
    if choice == "n":
        return loginmenu(user)
def addfunds(user):
    view.increase_balance_prompt()
    amount = view.increase_balance()
    if amount == 'exit':
        return loginmenu(user)
    if amount[0] == "$":
        amount = amount[1:]
    try:
        amount = float(amount)
    except ValueError:
        view.wrongchoice()
        return returnloop(user)
    view.creditcard_prompt()
    cardnumber = view.enter_creditcard()
    if not cardnumber.isdigit():
        view.invalid_creditcard()
        return returnloop(user)
    if not model.luhn_check(cardnumber):
        view.invalid_creditcard()
        return returnloop(user)
    user.increase_balance(amount)
    balance = user.getbalance()
    view.deposit_accepted(balance)
    return returnloop(user)
def viewportfolio(user):
    positions = user.getpositions()
    if len(positions) == 1:
        view.empty_portfolio()
        return returnloop(user)
    view.showpositions(positions)
    return returnloop(user)
def viewtransactions(user):
    view.transaction_history_prompt()
    choice = view.choose_transaction_history()
    while choice not in ["exit", "1", "2"]:
        view.wrongchoice()
        choice = view.choose_transaction_history()
    if choice == "exit":
        return loginmenu(user)
    if choice == "1":
        view.stock_pick_prompt()
        choice = view.stock_pick()
        choice = ticker_cap(choice)
        if not model.apiget(choice):
            view.stock_doesnt_exist()
            return returnloop(user)
        transactions = user.gettradesfor(choice)
        if not transactions:
            view.no_history(choice)
            return returnloop(user)
        view.show_transactions(transactions)
        return returnloop(user)
    if choice == "2":
        transactions = user.gettrades_display()
        if not transactions:
            view.no_transaction_history()
            return returnloop(user)
        view.showpositions(transactions)
        return returnloop(user)
def stockprices(user):
    view.stock_pick_prompt()
    ticker = view.stock_pick()
    price = model.apiget(ticker)
    if not price:
        view.stock_doesnt_exist()
        return returnloop(user)
    view.show_stock_price(ticker, price)
    view.buy_sell_from_price_ask(ticker)
    choice = view.buy_sell_from_price_choice()
    while choice not in ["y","n"]:
        view.wrongchoice()
        return returnloop(user)
    if choice == "y":
        return execute_trade_from_stock_view(user, ticker)
    if choice == "n":
        return returnloop(user)
    return returnloop(user)
def executetrade(user):
    view.buy_or_sell_prompt()
    choice = view.buy_or_sell_choice()
    while choice not in ["exit", "1", "2"]:
        view.wrongchoice()
        view.buy_or_sell_prompt()
        choice = view.buy_or_sell_choice()
    if choice == "exit":
        return loginmenu(user)
    if choice == "1":
        view.stock_pick_prompt()
        ticker = view.stock_pick()
        if not model.apiget(ticker):
            view.stock_doesnt_exist()
            return returnloop(user)
        price = model.apiget(ticker)
        ticker = ticker_cap(ticker)
        view.buy_volume_prompt(ticker, price)
        volume = view.buy_volume_ask()
        try:
            volume = int(volume)
        except ValueError:
            view.wrongchoice()
            return returnloop(user)
        if not zero_check(volume):
            view.wrongchoice()
            return returnloop(user)
        balance_check = user.sufficient_balance_check(float(price)*float(volume))
        if not balance_check:
            view.insufficient_balance()
            return returnloop(user)
        view.execute_buy_prompt(price, volume)
        choice = view.execute_trade()
        while choice not in ["y", "n"]:
            view.wrongchoice()
            view.execute_trade_prompt()
            choice = view.execute_trade()
        if choice == "y":
            user.buy(ticker, volume, price=price)
            view.buy_success()
            position = user.getposition(ticker)
            position_display = user.getposition_display(position, price=price)
            view.showposition(position_display)
            return returnloop(user)
        if choice == "n":
            view.trade_cancelled()
            return returnloop(user)
    if choice == "2":
        view.stock_pick_prompt()
        ticker = view.stock_pick()
        ticker = ticker_cap(ticker)
        if not model.apiget(ticker):
            view.stock_doesnt_exist()
            return returnloop(user)
        price = model.apiget(ticker)
        if not user.stock_ownership_check(ticker):
            view.stock_not_owned(ticker)
            return returnloop(user)
        view.sell_volume_prompt(ticker, price)
        volume = view.sell_volume_ask()
        try:
            volume = int(volume)
        except ValueError:
            view.wrongchoice()
            return returnloop(user)
        if not zero_check(volume):
            view.wrongchoice()
            return returnloop(user)
        if not user.sufficient_amount_check(ticker, volume):
            view.insufficient_amount_owned()
            return returnloop(user)
        view.execute_sell_prompt(price, volume)
        choice = view.execute_trade()
        while choice not in ["y", "n"]:
            view.wrongchoice()
            view.execute_trade_prompt()
            choice = view.execute_trade()
        if choice == "y":
            user.sell(ticker, volume, price=price)
            position = user.getposition(ticker)
            position = user.getposition_display(position, price=price)
            if position:
                view.sell_success()
                view.showposition(position)
            elif not position:
                view.position_closed()
                return returnloop(user)
            return returnloop(user)
        if choice == "n":
            view.trade_cancelled()
            return returnloop(user)
def adminaccountviewer(user):
    accounts = user.getaccounts()
    view.showaccounts(accounts)
    return returnloop(user)
def exit():
    view.goodbye()
    quit()

def returnloop(user):
    view.return_ask()
    choice = view.returnchoice()
    while choice not in ["y", "n"]:
        view.wrongchoice()
        view.return_ask()
        choice = view.returnchoice()
    if choice == "y":
        loginmenu(user)
    elif choice == "n":
        view.goodbye()
        quit()

def execute_trade_from_stock_view(user, ticker):
    view.buy_or_sell_prompt()
    choice = view.buy_or_sell_choice()
    while choice not in ["exit", "1", "2"]:
        view.wrongchoice()
        view.buy_or_sell_prompt()
        choice = view.buy_or_sell_choice()
    if choice == "exit":
        return loginmenu(user)
    if choice == "1":
        if not model.apiget(ticker):
            view.stock_doesnt_exist()
            return returnloop(user)
        price = model.apiget(ticker)
        ticker = ticker_cap(ticker)
        view.buy_volume_prompt(ticker, price)
        volume = view.buy_volume_ask()
        try:
            volume = int(volume)
        except ValueError:
            view.wrongchoice()
            return returnloop(user)
        if not zero_check(volume):
            view.wrongchoice()
            return returnloop(user)
        balance_check = user.sufficient_balance_check(float(price)*float(volume))
        if not balance_check:
            view.insufficient_balance()
            return returnloop(user)
        view.execute_buy_prompt(price, volume)
        choice = view.execute_trade()
        while choice not in ["y", "n"]:
            view.wrongchoice()
            view.execute_trade_prompt()
            choice = view.execute_trade()
        if choice == "y":
            user.buy(ticker, volume, price=price)
            view.buy_success()
            position = user.getposition(ticker)
            position_display = user.getposition_display(position, price=price)
            view.showposition(position_display)
            return returnloop(user)
        if choice == "n":
            view.trade_cancelled()
            return returnloop(user)
    if choice == "2":
        ticker = ticker_cap(ticker)
        if not model.apiget(ticker):
            view.stock_doesnt_exist()
            return returnloop(user)
        price = model.apiget(ticker)
        if not user.stock_ownership_check(ticker):
            view.stock_not_owned(ticker)
            return returnloop(user)
        view.sell_volume_prompt(ticker, price)
        volume = view.sell_volume_ask()
        try:
            volume = int(volume)
        except ValueError:
            view.wrongchoice()
            return returnloop(user)
        if not zero_check(volume):
            view.wrongchoice()
            return returnloop(user)
        if not user.sufficient_amount_check(ticker, volume):
            view.insufficient_amount_owned()
            return returnloop(user)
        view.execute_sell_prompt(price, volume)
        choice = view.execute_trade()
        while choice not in ["y", "n"]:
            view.wrongchoice()
            view.execute_trade_prompt()
            choice = view.execute_trade()
        if choice == "y":
            user.sell(ticker, volume, price=price)
            position = user.getposition(ticker)
            position = user.getposition_display(position, price=price)
            if position:
                view.sell_success()
                view.showposition(position)
            elif not position:
                view.position_closed()
                return returnloop(user)
            return returnloop(user)
        if choice == "n":
            view.trade_cancelled()
            return returnloop(user)

def zero_check(num):
    number = str(num)
    for i in number:
        if i != "0":
            return True
    return False

def ticker_cap(string):
    ticker = []
    for i in string:
        ticker.append(i.capitalize())
    ticker = "".join(ticker)
    return ticker
    
def run():
    view.clear()
    initialmenu()

while __name__ == "__main__":
    run()
    
