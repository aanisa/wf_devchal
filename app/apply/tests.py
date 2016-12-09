import unittest
import models
import flask
from app import app, db
import os

class TestCase(unittest.TestCase):
    def setUp(self):
        # reset db
        db.reflect()
        db.drop_all()
        db.create_all()
        XXX RUN seed
        # sensible defalts
        self.guid = models.responses()["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        assert isinstance(models.Survey().data, dict)

    def test_response(self):
        response = models.Response(self.guid)
        assert isinstance(response.data, dict)
        assert len(response.schools) > 0

    def test_appointment(self):
        assert False

    def test_after_survey_monkey(self):
        assert False

    def test_calendly_webhook(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            data = f.read()
        with app.test_request_context():
            response = app.test_client().post(flask.url_for('apply_blueprint.calendly_webhook'), data=data, content_type='application/json')
