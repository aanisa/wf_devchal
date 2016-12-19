import unittest
import models
import flask
from app import app, db, mail
import os
from . import seed
import click
from click.testing import CliRunner
import json

blueprint_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit() # fixes hang - see http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
        r = CliRunner().invoke(seed)
        if r.exception: raise r.exception
        self.guid = models.responses(1)["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        self.assertIsInstance(models.Survey().data, dict)

    def test_response(self):
        response = models.Response(guid=self.guid)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.schools), 0)

    def test_checklist(self):
        models.Response(guid=self.guid).create_checklists()
        checklist = models.Checklist.query.first()
        with app.app_context():
            with mail.record_messages() as outbox:
                checklist.email_checklist()
                self.assertGreater(len(outbox), 0)
        self.assertIsNone(checklist.visit_scheduled_at)
        checklist.completed("visit")
        self.assertIsNotNone(checklist.visit_scheduled_at)

    def test_appointment(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            a = models.Appointment(json.loads(f.read()))
        self.assertIsInstance(a.school, models.School)

    def test_redirect_to_survey_monkey_with_guid(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.redirect_to_survey_monkey_with_guid".format(blueprint_name)))

    def test_after_survey_monkey(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.after_survey_monkey".format(blueprint_name)) + "guid=1234")

    def test_calendly_webhook(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            data = f.read()
        with app.test_request_context():
            response = app.test_client().post(flask.url_for("{0}.calendly_webhook".format(blueprint_name)), data=data, content_type='application/json')

    def test_completed(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.completed".format(blueprint_name)) + "?guid=1234&id=1")

    def test_school_schema(self):
        # not sure why this requires test_request_context
        with app.test_request_context():
            print models.SchoolSchema().dump(models.School.query.get(1)).data
