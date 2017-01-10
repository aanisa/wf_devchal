import unittest
import models
import flask
from app import app, db, mail
import os
import cli
from click.testing import CliRunner
import json
import flask_restful

blueprint_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit() # fixes hang - see http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
        r = CliRunner().invoke(cli.seed)
        if r.exception: raise r.exception
        self.guid = models.SurveyMonkey.responses(1)["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        s = models.Survey()
        self.assertIsInstance(s.data, dict)
        self.assertIsInstance(s.questions, list)
        self.assertIsInstance(s.questions[0], models.SurveyMonkey.Question)

    def test_response(self):
        response = models.SurveyMonkey.Response(guid=self.guid)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.schools), 0)
        with app.app_context():
            with mail.record_messages() as outbox:
                response.email_response()
                i = len(outbox)
                self.assertGreater(i, 0)
                checklist.email_next_steps()
                self.assertGreater(len(outbox), i)

    def test_redirect_to_survey_monkey_with_guid(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.redirect_to_survey_monkey_with_guid".format(blueprint_name)))
            self.assertEqual(response.status_code, 200)

    def test_after_survey_monkey(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.after_survey_monkey".format(blueprint_name)) + "guid={0}".format(self.guid))
            self.assertEqual(response.status_code, 200)

    def test_non_text_answer(self):
        r = models.SurveyMonkey.Response(guid=self.guid)
        assert r.answer_for(app.config['ANSWER_KEY']['CHILD']['GENDER']['SURVEY_MONKEY'])

    def test_transparent_classroom_submit_application(self):
        r = models.SurveyMonkeyResponse(guid=self.guid)
        self.assertIsInstance(i, models.TransparentClassroom(3).submit_application(r, "Children's House: Morning Program (8:30a-12:30p)"))
