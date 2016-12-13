import unittest
import models
import flask
from app import app, db
import os
from . import seed
import click
from click.testing import CliRunner
import json

class TestCase(unittest.TestCase):
    def setUp(self):
        db.reflect()
        db.drop_all()
        db.create_all()
        print CliRunner().invoke(seed).output
        self.guid = models.responses(1)["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        assert isinstance(models.Survey().data, dict)

    def test_response(self):
        response = models.Response(guid=self.guid)
        assert isinstance(response.data, dict)
        assert len(response.schools) > 0

    def test_appointment(self):
        print models.School.query.all()
        # with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
        #     a = models.Appointment(json.loads(f.read()))
        # print a.data["payload"]["event"]["extended_assigned_to"][0]["email"]
        # print a.school

    def test_after_survey_monkey(self):
        assert False

    def test_calendly_webhook(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            data = f.read()
        with app.test_request_context():
            response = app.test_client().post(flask.url_for('apply_blueprint.calendly_webhook'), data=data, content_type='application/json')
