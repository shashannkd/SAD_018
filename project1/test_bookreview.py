import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from test_methods import getbook,review_exists


class TestReview(unittest.TestCase):

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

    def test_review_exits(self):
        flag = review_exists('user1','')
        self.assertTrue(flag)

    def test_invalid_review(self):
        flag = review_exists('user2', '1857231082')
        self.assertFalse(flag)

    def test_review(self):
        flag = review_exists('user1','0380795272')
        self.assertTrue(flag)

if __name__ == "__main__":
    unittest.main()