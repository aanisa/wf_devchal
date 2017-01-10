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
        self.guid = models.responses(1)["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        self.assertIsInstance(models.Survey().data, dict)
        self.assertIsInstance(models.Survey().questions, list)
        self.assertIsInstance(models.Survey().questions[0], models.Question)

    def test_response(self):
        response = models.Response(guid=self.guid)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.schools), 0)
        with app.app_context():
            with mail.record_messages() as outbox:
                response.email_response()
                self.assertGreater(len(outbox), 0)

    def test_checklist(self):
        models.Response(guid=self.guid).create_checklists()
        checklist = models.Checklist.query.first()
        with app.app_context():
            with mail.record_messages() as outbox:
                checklist.email_checklist()
                self.assertGreater(len(outbox), 0)
        self.assertIsNone(checklist.child_visit_scheduled_at)
        checklist.completed("child_visit")
        self.assertIsNotNone(checklist.child_visit_scheduled_at)

    def test_appointment(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            a = models.Appointment(json.loads(f.read()))
        self.assertIsInstance(a.school, models.School)

    def test_redirect_to_survey_monkey_with_guid(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.redirect_to_survey_monkey_with_guid".format(blueprint_name)))
            self.assertEqual(response.status_code, 200)

    def test_after_survey_monkey(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.after_survey_monkey".format(blueprint_name)) + "guid={0}".format(self.guid))
            self.assertEqual(response.status_code, 200)

    def test_calendly_webhook(self):
        with open("{0}/calendly_sample.json".format(os.path.dirname(os.path.realpath(__file__))), 'r') as f:
            data = f.read()
        with app.test_request_context():
            response = app.test_client().post(flask.url_for("{0}.calendly_webhook".format(blueprint_name)), data=data, content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_completed(self):
        with app.test_request_context():
            response = app.test_client().get(flask.url_for("{0}.completed".format(blueprint_name)) + "?guid={0}&id=1".format(self.guid))
            self.assertEqual(response.status_code, 200)

    def test_school_resource(self):
        with app.test_request_context():
            response = app.test_client().get(flask_restful.url_for("{0}.schoolresource".format(blueprint_name), school_id=1))
            self.assertEqual(response.status_code, 200)

    def test_response_schema(self):
        with app.test_request_context():
            s = json.loads(models.ResponseSchema().jsonify(models.Response(guid=self.guid)).data)
            self.assertIsInstance(s["parents"], list)
            self.assertIsInstance(s["child"], dict)


    def test_checklist_schema(self):
        with app.test_request_context():
            s = json.loads(models.ChecklistSchema().jsonify(models.Checklist.query.first()).data)
            self.assertIsInstance(s["response"], dict)

    def test_school_schema(self):
        with app.test_request_context():
            s = json.loads(models.SchoolSchema().jsonify(models.School.query.first()).data)
            self.assertIsInstance(s["checklists"], list)

    def test_non_text_answer(self):
        r = models.Response(guid=self.guid)
        assert r.answer_for(app.config['ANSWER_KEY']['CHILD']['GENDER']['SURVEY_MONKEY'])

    def test_tcapi_submit_application(self):
        r = models.Response(guid=self.guid)
        models.TCAPI("hy4385yczauTVD66ufUC", 3).submit_application(r, "Children's House: Morning Program (8:30a-12:30p)")
