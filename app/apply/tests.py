import unittest
import models
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        # TODO - delete all data from tables
        pass

    def test_foo(self):
        c = models.School(name="Name")
        db.session.add(c)
        db.session.commit()
        assert True
