import unittest
from models import School
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        # TODO - delete all data from tables
        pass

    def test_foo(self):
        c = School(name="Name")
        db.session.add(c)
        db.session.commit()
        assert True
