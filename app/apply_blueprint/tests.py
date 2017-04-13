import unittest
import models
import flask
from app import app, db, mail
import os
import cli
from click.testing import CliRunner
import types

blueprint_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit() # fixes hang - see http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
        r = CliRunner().invoke(cli.seed)
        if r.exception: raise r.exception
        self.guid = models.SurveyMonkey.Response.responses("sandbox", "foo")["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        s = models.SurveyMonkey.Survey("sandbox")
        self.assertIsInstance(s.data, dict)
        self.assertIsInstance(s.pages, list)
        self.assertIsInstance(s.pages[0].questions, list)
        self.assertIsInstance(s.pages[0].questions[0], models.SurveyMonkey.Survey.Question)

    def test_response(self):
        response = models.SurveyMonkey.Response("sandbox", guid=self.guid)
        self.assertIsInstance(response.data, dict)

    def test_application(self):
        response = models.SurveyMonkey.Response("sandbox", guid=self.guid)
        application = models.Application(response)
        self.assertIsInstance(application.children, list)
        self.assertIsInstance(application.parents, list)
        self.assertIsInstance(application.answers, list)
        self.assertIsInstance(application.children[0].answers, list)
        application.submit_to_transparent_classroom()
        with app.app_context():
            with mail.record_messages() as outbox:
                application.email_schools()
                i = len(outbox)
                self.assertGreater(i, 0)
                i = 0
                application.email_parent()
                self.assertGreater(len(outbox), i)

    def test_redirect_to_survey_monkey_with_guid(self):
        with app.test_request_context():
            url = flask.url_for("{0}.redirect_to_survey_monkey_with_guid".format(blueprint_name), hub="sandbox")
            response = app.test_client().get(url)
            self.assertEqual(response.status_code, 200)

    def test_after_survey_monkey(self):
        with app.test_request_context():
            url = flask.url_for("{0}.after_survey_monkey".format(blueprint_name)) + "?hub=sandbox&response_guid={0}".format(self.guid)
            response = app.test_client().get(url)
            self.assertEqual(response.status_code, 200)

    def test_application_breaks_transparent_classroom_validations(self):
        response = models.SurveyMonkey.Response("sandbox", guid=self.guid)
        application = models.Application(response)
        application.parents[0].phone.value = "XYZ"
        application.submit_to_transparent_classroom()
