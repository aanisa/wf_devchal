from app import app, db, ma, mail
import sqlalchemy.orm
from functools32 import lru_cache
import datetime
import requests
from combomethod import combomethod
import inspect
import dateutil.parser
import os
from sqlalchemy.ext.hybrid import hybrid_property
from flask_mail import Message
from flask import render_template
import json
import re

tablename_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class School(Base):
    __tablename__ = "{0}_school".format(tablename_prefix)
    tc_school_id = db.Column(db.Integer)
    tc_session_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    match = db.Column(db.String(80))
    schedule_parent_teacher_conversation_url = db.Column(db.String(80))
    parent_teacher_conversation_optional = db.Column(db.Boolean())
    schedule_parent_observation_url = db.Column(db.String(80))
    parent_observation_optional = db.Column(db.Boolean())
    schedule_child_visit_url = db.Column(db.String(80))
    child_visit_optional = db.Column(db.Boolean())
    email = db.Column(db.String(80))
    hub = db.Column(db.String(80))

class SurveyMonkey(object):
    # log SurveyMonkey's X-Ratelimit-App-Global-Day-Remaining header
    # the http library uses stdout for logging, not the logger, so you can't
    # reasonably filter it's output; having *all* the headers is too much
    # consequently, I'm subclassing the request library and having the get
    # method (the only one I'm currently using) do the logging
    class Session(requests.Session):
        def __init__(self):
            super(type(self), self).__init__()
            self.headers.update({
              "Authorization": "Bearer {0}".format(app.config['SURVEY_MONKEY_OAUTH_TOKEN']),
              "Content-Type": "application/json"
            })

        def get(self, url, params=None, **kwargs):
            response = super(type(self), self).get(url, params=None, **kwargs)
            if "X-Ratelimit-App-Global-Day-Remaining" in response.headers:
                app.logger.info("SurveyMonkey: X-Ratelimit-App-Global-Day-Remaining: {0}".format(response.headers["X-Ratelimit-App-Global-Day-Remaining"]))
            return response

    request_session = Session()

    class Survey():
        @classmethod
        @lru_cache(maxsize=None)
        def survey(cls, hub):
            return SurveyMonkey.request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/details".format(app.config['SURVEY_MONKEY_SURVEY_ID'])).json()
            # with open("{0}/sample-survey-monkey-survey-details.json".format(os.path.dirname(os.path.realpath(__file__))), 'rb') as f:
            #     self.data = json.load(f)

        def __init__(self, hub):
            self.data = SurveyMonkey.Survey.survey(hub)

        def value_for(self, question_id, choice_id):
            for page in self.data["pages"]:
                for question in page["questions"]:
                    if question["id"] == question_id:
                        for choice in question["answers"]["choices"]:
                            if choice["id"] == choice_id:
                                return choice["text"]
            raise LookupError

        class Page(object):
            def __init__(self, title):
                self.title = title
                self.questions = []

            def show_for(self, response):
                for question in self.questions:
                    if response.answers_for(question.id) != []:
                        return True
                return False

        class Question(object):
            def __init__(self, id, text):
                self.id = id
                self.text = text

            def show_for(self, response):
                if response.answers_for(self.id) != []:
                    return True
                return False

        @property
        def pages(self):
            pages = []
            for p in self.data["pages"]:
                page = SurveyMonkey.Survey.Page(p["title"])
                for question in p["questions"]:
                    page.questions.append(SurveyMonkey.Survey.Question(question["id"], question["headings"][0]["heading"]))
                pages.append(page)
            return pages

    class Response():
        # this is a classmethod so that it can be used in the tests
        @classmethod
        @lru_cache(maxsize=None)
        def responses(cls, key): # important to have the key for the caching to work properly
            return SurveyMonkey.request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/responses/bulk".format(app.config["SURVEY_MONKEY_SURVEY_ID"]),  params={"sort_order": "DESC"}).json()
            # with open("{0}/sample-survey-monkey-responses-bulk.json".format(os.path.dirname(os.path.realpath(__file__))), 'rb') as f:
            #     return json.load(f)

        def __init__(self, guid=None, email=None):
            for d in SurveyMonkey.Response.responses("{0}{1}".format(guid, email))["data"]:
                self.guid = d["custom_variables"]["response_guid"]
                if guid:
                    if d["custom_variables"]["response_guid"] == guid:
                        self.data = d
                        return
                elif email:
                    for page in d["pages"]:
                        for question in page["questions"]:
                            if question["id"] in [app.config['ANSWER_KEY']['PARENTS'][0]['EMAIL']['SURVEY_MONKEY'], app.config['ANSWER_KEY']['PARENTS'][1]['EMAIL']['SURVEY_MONKEY']]:
                                if question["answers"][0]["text"].lower() == email.lower():
                                    self.data = d
                                    return
            raise LookupError

        def email_next_steps(self):
            for school in self.schools:
                message = {
                    "subject": "Next steps for your application to {0}".format(school.name),
                    "sender": school.email,
                    "recipients": ["{0} {1} <{2}>".format(
                        SurveyMonkey.Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['FIRST_NAME']['SURVEY_MONKEY']),
                        SurveyMonkey.Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['LAST_NAME']['SURVEY_MONKEY']),
                        SurveyMonkey.Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['EMAIL']['SURVEY_MONKEY'])
                    )],
                    "bcc": ['dan.grigsby@wildflowerschools.org', 'cam.leonard@wildflowerschools.org'],
                    "html": render_template("email_next_steps.html", school=school)
                }
                mail.send(Message(**message))

        def email_response(self):
            message = {
                "subject": "Application for {0} {1}".format(self.answer_for(app.config['ANSWER_KEY']['CHILD']['FIRST_NAME']['SURVEY_MONKEY']), self.answer_for(app.config['ANSWER_KEY']['CHILD']['LAST_NAME']['SURVEY_MONKEY'])),
                "sender": "Wildflower Schools <noreply@wildflowerschools.org>",
                "recipients": [s.email for s in self.schools] + ['dan.grigsby@wildflowerschools.org', 'cam.leonard@wildflowerschools.org'],
                "html": render_template("email_response.html", response=self, survey=SurveyMonkey.Survey())
            }
            mail.send(Message(**message))

        def submit_to_transparent_classroom(self):
            for school in self.schools:
                TransparentClassroom(school.tc_school_id).submit_application(self)

        def raw_answers_for(self, question_id):
            for page in self.data["pages"]:
                for question in page["questions"]:
                    if question["id"] == question_id:
                        return question["answers"]
            return []

        def value_for(self, question_id, answer):
            if "text" in answer:
                return answer["text"]
            else:
                return re.sub('<[^<]+?>', '', SurveyMonkey.Survey().value_for(question_id, answer["choice_id"]))
            return None

        def answer_for(self, question_id):
            # http://stackoverflow.com/questions/363944/python-idiom-to-return-first-item-or-none
            return next(iter(self.answers_for(question_id) or []), None)

        def answers_for(self, question_id):
            raw_answers = self.raw_answers_for(question_id)
            answers = []
            for raw_answer in raw_answers:
                answers.append(self.value_for(question_id, raw_answer))
            return answers

        @property
        def schools(self):
            schools = []
            for answer in self.answers_for(app.config['ANSWER_KEY']['SCHOOLS']['SURVEY_MONKEY']):
                for school in School.query.all():
                    if answer.lower().find(school.match.lower()) >= 0:
                        schools.append(school)
            return schools

        def model_factory(self, class_name, d):
            class ModelFromFactory(): pass
            ModelFromFactory.__name__ = class_name
            m = ModelFromFactory()
            for k in d:
                setattr(m, k.lower(), self.answer_for(d[k]['SURVEY_MONKEY']))
            return m

        @property
        def parents(self):
            return [
                self.model_factory("Parent", app.config['ANSWER_KEY']['PARENTS'][0]),
                self.model_factory("Parent", app.config['ANSWER_KEY']['PARENTS'][1])
            ]

        @property
        def child(self):
            return self.model_factory("Child", app.config['ANSWER_KEY']['CHILD'])

class TransparentClassroom(object):
    def __init__(self, tc_school_id):
        self.base_url = "{0}/api/v1".format(app.config["TRANSPARENT_CLASSROOM_BASE_URL"])
        self.request_session = requests.session()
        self.request_session.headers.update({
          "X-TransparentClassroomToken": app.config['TRANSPARENT_CLASSROOM_API_TOKEN'],
          "Accept": "application/json",
          "Content-Type": "application/json",
          "X-TransparentClassroomSchoolId": "{0}".format(tc_school_id)
        })
        self.tc_school_id = tc_school_id

    def params_key(self, item, all):
        if type(item) == dict:
            if "TRANSPARENT_CLASSROOM" in item:
                all.append(item)
            else:
                for key in item:
                    all = self.params_key(item[key], all)
        elif type(item) == list:
            for i in item:
                all = self.params_key(i, all)
        return all

    def submit_application(self, response):
        tc_params = {
            "session_id": School.query.filter_by(tc_school_id=self.tc_school_id).first().tc_session_id,
            "program": "Default"
        }
        for item in self.params_key(app.config['ANSWER_KEY'], []):
            answer = response.answer_for(item['SURVEY_MONKEY'])
            if answer:
                tc_params[item['TRANSPARENT_CLASSROOM']] = answer
        response = self.request_session.post("{0}/online_applications.json".format(self.base_url), data=json.dumps({"fields": tc_params}))
        if response.status_code != 201:
            raise LookupError, response.body
