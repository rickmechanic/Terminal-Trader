from time import time
from random import randint
import sqlite3
import werkzeug
import requests


DBNAME = "ttrader.db"

def apiget(tick, url="https://api.iextrading.com/1.0/stock/{}/quote"):
    URL = url.format(tick)
    try:
        data = requests.get(URL).json()
        price = data.get("latestPrice")
    except:
        price = None
    return price

class OpenCursor:

    def __init__(self, db=DBNAME, *args, **kwargs):
        self.conn = sqlite3.connect(db, *args, **kwargs)
        self.conn.row_factory = sqlite3.Row  # access fetch results by col name
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, extype, exvalue, extraceback):
        if not extype:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


class Position:

    def __init__(self, account_pk=None, ticker=None, amount=None, pk=None):
        self.account_pk = account_pk
        self.ticker = ticker
        self.amount = amount
        self.pk = pk

    def save(self):
        with OpenCursor() as cur:
            if not self.pk:
                SQL = """
                INSERT INTO positions(account_pk, ticker, amount)
                VALUES(?, ?, ?);
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.amount))
                self.pk = cur.lastrowid

            else:
                SQL = """
                UPDATE positions SET account_pk=?, ticker=?, amount=? WHERE
                pk=?;
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.amount,
                                  self.pk))

    def set_from_row(self, row):
        self.pk = row["pk"]
        self.account_pk = row["account_pk"]
        self.ticker = row["ticker"]
        self.amount = row["amount"]
        return self

    def getvalue(self):
        return self.amount * apiget(self.ticker)

    def __repr__(self):
        display = "Position PK = {}: Stock = {}, Amount = {}, Account PK = {}".format(self.pk, self.ticker, self.amount, self.account_pk)
        return display


class Trade:

    def __init__(self, pk=None, account_pk=None, ticker=None,
                 volume=None, price=None, time=None):
        self.pk = pk
        self.account_pk = account_pk
        self.ticker = ticker
        self.volume = volume
        self.price = price
        self.time = time

    def save(self):
        if self.time is None:
            self.time = int(time())
        with OpenCursor() as cur:
            if not self.pk:
                SQL = """
                INSERT INTO trades (account_pk, ticker, volume, price, time)
                VALUES(?, ?, ?, ?, ?);
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.volume, self.price, self.time))
                self.pk = cur.lastrowid

            else:
                SQL = """
                UPDATE trades SET account_pk=?, ticker=?, volume=?, price=?, time=? WHERE
                pk=?;
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.volume, self.price, self.time,
                                  self.pk))

    def set_from_row(self, row):
        self.pk = row["pk"]
        self.account_pk = row["account_pk"]
        self.ticker = row["ticker"]
        self.volume = row["volume"]
        self.price = row["price"]
        self.time = row["time"]
        return self

    def __repr__(self):
        display = "Trade PK = {}: Time = {}, Stock = {}, Price = {}, Volume = {}, Account PK = {}".format(self.pk, self.time, self.ticker, self.price, self.volume, self.account_pk)
        return display

class Account:

    def __init__(self, username=None, pass_hash=None, balance=None, pk=None):
        self.pk = pk
        self.username = username
        self.pass_hash = pass_hash
        self.balance = balance
        

    def save(self):
        with OpenCursor() as cur:
            if not self.pk:
                SQL = """
                INSERT INTO accounts(username, pass_hash, balance)
                VALUES(?, ?, ?);
                """
                cur.execute(SQL, (self.username, self.pass_hash, self.balance))
                self.pk = cur.lastrowid

            else:
                SQL = """
                UPDATE accounts SET username=?, pass_hash=?, balance=? WHERE
                pk=?;
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.amount,
                                  self.pk))

    def set_from_row(self, row):
        self.pk = row["pk"]
        self.username = row["username"]
        self.pass_hash = row["pass_hash"]
        self.balance = row["balance"]
        return self

    def set_from_pk(self, pk):
        with OpenCursor() as cur:
            """ given a pk, get the row of that user from the database and pass it
            to set_from_row"""
            SQL = """
            SELECT * FROM accounts WHERE accounts.pk=?"""
            cur.execute(SQL, (pk,))
            row = cur.fetchone()
        return self.set_from_row(row)
    
    def getpositions(self):
        with OpenCursor() as cur:
            SQL = """
            SELECT * FROM positions WHERE account_pk=?"""
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
            results = []
            for row in rows:
                pos = Position()
                pos.set_from_row(row)
                results.append(pos)
        return results
    
    def getposition(self, ticker):
        with OpenCursor() as cur:
            SQL = """
            SELECT * FROM positions WHERE account_pk=? AND ticker=?"""
            cur.execute(SQL, (self.pk,ticker))
            row = cur.fetchone()
            if not row:
                return None
            pos = Position()
        return pos.set_from_row(row)
    
    def increase_position(self, ticker, amount):
        pos = self.getposition(ticker)
        if not pos:
            pos = Position(account_pk=self.pk, ticker=ticker, amount=0)
        pos.amount += amount
        pos.save()
    
    def decrease_position(self, ticker, amount):
        pos = self.getposition(ticker)
        if not pos or pos.amount < amount:
            raise ValueError("Position doesn't exist or insufficient amount")
        pos.amount -= amount
        pos.save()
    
    def gettrades(self):
        with OpenCursor() as cur:
            SQL = """
            SELECT * FROM trades WHERE account_pk=? ORDER BY time DESC"""
            cur.execute(SQL, (self.account_pk,))
            row = cur.fetchall()
            results = []
            for row in rows:
                trade = Trade()
                pos.set_from_row(row)
                results.append(pos)
        return pos.set_from_row(row)
    
    def gettradesfor(self, ticker):
        with OpenCursor() as cur:
            SQL = """
            SELECT * FROM trades WHERE account_pk=? AND ticker=? ORDER BY time DESC"""
            cur.execute(SQL, (self.pk, ticker))
            rows = cur.fetchall()
            results = []
            for row in rows:
                trade = Trade()
                trade.set_from_row(row)
                results.append(trade)
        return results
    
    #TODO: def createtrade():

    def sell(self, ticker, volume, price=None):
        if price is None:
            price = apiget(ticker)
        try:
            decrease_position(ticker, amount=volume)
            trade=Trade(account_pk=self.account_pk, ticker=ticker, volume=volume*-1, price=price)
            self.balance += volume*price
            trade.save()
            self.save()
        except ValueError:
            return None
    
    def buy(self, ticker, volume, price=None):
        if price is None:
            price = apiget(ticker)
        try:
            increase_position(ticker, amount=volume)
            trade=Trade(account_pk=self.pk, ticker=ticker, volume=volume, price=price)
            self.balance += volume*price
            trade.save()
            self.save()
        except ValueError:
            return None
            


