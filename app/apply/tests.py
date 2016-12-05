import unittest
import models
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        # reset db
        db.reflect()
        db.drop_all()
        db.create_all()
        # sensible defalts
        self.guid = models.responses()["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        assert isinstance(models.Survey().data, dict)

    def test_response(self):
        response = models.Response(self.guid)
        assert isinstance(response.data, dict)
        assert len(response.schools()) > 0
