import os
import unittest
import model_test
import schema
import testseed

TESTDB = "__TEST.DB"
model_test.CONFIG['DBNAME'] = TESTDB

model_test.DBNAME="test.db"

class TestCursor(unittest.TestCase):

    def setUp(self):
        schema.setup(TESTDB)
        schema.run()
        testseed.setup(TESTDB)
        testseed.run()
    
    def tearDown(self):
        os.remove(TESTDB)

    def testAPI(self):
        price = model_test.apiget("AAPL")
        self.assertEqual(type(price), float, "API did not return a float")
        self.assertTrue(price > 0.0, "API returned a negative number")
    
    def testBadBuy(self):
        u = model_test.Account()
        u.set_from_pk(2)
        balance = u.getbalance()
        buy = u.buy("AAPL",500000)
        self.assertFalse(buy, "Buy should not be executed")
        self.assertEqual(u.getbalance(),balance, "Bad Trade should not affect original balance")
    
    def testBadSell(self):
        u = model_test.Account()
        u.set_from_pk(1)
        sale = u.sell("AAPL",11)
        pos = u.getposition("AAPL")
        self.assertFalse(sale, "Sale should not be executed")
        self.assertEqual(pos.amount, 10, "Cancelled sale shouldn't affect balance")
    
    def testLuhn(self):
        a = model_test.luhn_check("1")
        b = model_test.luhn_check(str(4010101010101010))
        c = model_test.luhn_check(str(5156769966067548))
        e = model_test.luhn_check(str(5156769966067549))
        d = model_test.luhn_check(str(1234567890123456))
        self.assertFalse(a, "Luhn failed length")
        self.assertFalse(b, "Luhn failed Visa")
        self.assertFalse(c, "Luhn failed Mastercard")
        self.assertFalse(d, "Luhn straight up failed")
        self.assertTrue(e, "Luhn straight up failed")
    
    def testPortfolioView(self):
        u = model_test.Account()
        u.set_from_pk(1)
        port = u.getpositions()
        self.assertEqual((len(port)), 2, "Portfolio view doesn't show entire portfolio")
    
    def testIncreasePosition(self):
        u = model_test.Account()
        u.set_from_pk(1)
        u.increase_position("F", 10)
        pos = u.getposition("F")
        self.assertEqual(pos.amount, 10, "Increase position didn't create position")
        v = model_test.Account()
        v.set_from_pk(1)
        v.increase_position("AAPL", 10)
        pos = v.getposition("AAPL")
        self.assertEqual(pos.amount, 20, "Increase position didn't update existing position")
        apos = v.getpositions()
        self.assertEqual(len(apos), 3, "Increase positions didn't work")
    
    def testAdminAttribute(self):
        u = model_test.Account()
        u.set_from_pk(2)
        self.assertEqual(u.acct_type, "ADMN", "Admin account doesn't have a 'type' attribute")
