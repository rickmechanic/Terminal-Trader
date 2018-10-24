from time import time
from random import randint
import sqlite3
import werkzeug

DBNAME = "ttrader.db"

# TODO: implement API lookup of stock price


def getprice(symbol):
    return randint(5000, 20000) / 100


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
        return self.amount * getprice(self.ticker)


class Trade:
    def __init__(self, account_pk=None, ticker=None,
                 volume=None, price=None, time=None):
        self.account_pk = account_pk,
        self.ticker = ticker,
        self.volume = volume,
        self.price = price,
        self.time = time

    def save(self):
        if self.time is None:
            self.time = int(time())

    def set_from_row(self, row):
        return self


class Account:
    def __init__(self, username=None, password_hash=None, balance=None, pk=None):
        self.pk = pk
        self.username = username
        self.password_hash = password_hash
        self.balance = balance
        

    def save(self):
        with OpenCursor() as cur:
            if not self.pk:
                SQL = """
                INSERT INTO accounts(username, password_hash, balance)
                VALUES(?, ?, ?);
                """
                cur.execute(SQL, (self.username, self.password_hash, self.balance))
                self.pk = cur.lastrowid

            else:
                SQL = """
                UPDATE accounts SET username=?, password_hash=?, balance=? WHERE
                pk=?;
                """
                cur.execute(SQL, (self.account_pk, self.ticker, self.amount,
                                  self.pk))

    def set_from_row(self, row):
        self.pk = row["pk"]
        self.username = row["username"]
        self.password_hash = row["password_hash"]
        self.balance = row["balance"]
        return self

    def set_from_pk(self, pk):
        with OpenCursor() as cur:
            """ given a pk, get the row of that user from the database and pass it
            to set_from_row"""
            SQL = """
            SELECT * FROM accounts WHERE accounts.pk=pk"""
            cur.execute(SQL)
            row = cur.fetchone()
        return self.set_from_row(row)

