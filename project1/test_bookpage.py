import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from test_methods import getbook


class TestBookpage(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy()
        db.init_app(app)
        app.app_context().push()
     # Returns True or False.
    def test(self):
        self.assertTrue(True)

    # executed after each test
    def tearDown(self):
        pass

###############
#### tests ####
###############

    def test_title(self):
        book = getbook('081299289X')
        self.assertEqual(book.title,'China Dolls')

    def test_author(self):
        book = getbook('0345498127')
        self.assertEqual(book.author,'David Nicholls')

    def test_year(self):
        book = getbook('0061053716')
        self.assertEqual(book.year,'1991')

    def test_isbn(self):
        book = getbook('006105371')
        self.assertEqual(book,None)

if __name__ == "__main__":
    unittest.main()
