import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from test_methods import getbook,getSearchDetails


class TestSearch(unittest.TestCase):

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

    def test_isbnSearch(self):
        data = getSearchDetails("0380795272","ISBN")
        self.assertEqual(data.title, "Krondor: The Betrayal")

    def test_titleSearch(self):
        data = getSearchDetails("Dark Is Rising","Title")
        self.assertEqual(data.title, "The Dark Is Rising")

    def test_authorSearch(self):
        data = getSearchDetails("Terry","Author")
        self.assertEqual(data.title, "The Black Unicorn ")

    def test_invalid(self):
        data = getSearchDetails("1234","ISBN")
        self.assertEqual(len(data), 0)

if __name__ == "__main__":
    unittest.main()