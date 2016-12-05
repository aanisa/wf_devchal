import unittest
import models
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        # reset db
        db.reflect()
        db.drop_all()
        db.create_all()

    def test_foo(self):
        assert True
