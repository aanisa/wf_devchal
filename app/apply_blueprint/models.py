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
    name = db.Column(db.String(120))
    match = db.Column(db.String(120))
    schedule_parent_teacher_conversation_url = db.Column(db.String(120))
    parent_teacher_conversation_optional = db.Column(db.Boolean())
    schedule_parent_observation_url = db.Column(db.String(120))
    parent_observation_optional = db.Column(db.Boolean())
    schedule_child_visit_url = db.Column(db.String(120))
    child_visit_optional = db.Column(db.Boolean())
    email = db.Column(db.String(120))
    hub = db.Column(db.String(120))

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
            return SurveyMonkey.request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/details".format(app.config['HUBS'][hub.upper()]['SURVEY_MONKEY_SURVEY_ID'])).json()
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
                self.validator = validator

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
        def responses(cls, hub, key): # important to have the key for the caching to work properly
            return SurveyMonkey.request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/responses/bulk".format(app.config['HUBS'][hub.upper()]['SURVEY_MONKEY_SURVEY_ID']),  params={'sort_order': 'DESC'}).json()

        def __init__(self, hub, guid=None, email=None):
            self.hub = hub
            for d in SurveyMonkey.Response.responses(self.hub, "{0}{1}".format(guid, email))["data"]:
                self.guid = d["custom_variables"]["response_guid"]
                if guid:
                    if d["custom_variables"]["response_guid"] == guid:
                        self.data = d
                        return
                elif email:
                    for page in d["pages"]:
                        for question in page["questions"]:
                            if question["id"] in [app.config['HUBS'][self.hub.upper()]['ANSWER_KEY']['parents'][0]['email']['survey_monkey'], app.config['HUBS'][self.hub.upper()]['ANSWER_KEY']['parents'][1]['email']['survey_monkey']]:
                                if question["answers"][0]["text"].lower() == email.lower():
                                    self.data = d
                                    return
            raise LookupError

        def value_for(self, question_id, answer):
            if "text" in answer:
                return answer["text"]
            else:
                return re.sub('<[^<]+?>', '', SurveyMonkey.Survey(self.hub).value_for(question_id, answer["choice_id"]))
            return None

        def values_for(self, question_id):
            values = []
            for page in self.data["pages"]:
                for question in page["questions"]:
                    if question["id"] == question_id:
                        for raw_answer in question["answers"]:
                            values.append(self.value_for(question_id, raw_answer))
            return values

        class Answer(object):
            def __init__(self, value, survey_monkey_question_id, transparent_classroom_key, validator):
                self.value = value
                self.survey_monkey_question_id = survey_monkey_question_id
                self.transparent_classroom_key = transparent_classroom_key
                self.validator = validator

            def __str__(self):
                return self.value

        class Answers(object)
            def __init__(self, response, item):
                self.response = response
                self.answers_factory(item)

            def answers_factory(item):
                if type(item) == dict:
                    if "TRANSPARENT_CLASSROOM" in item:
                        return Answer(self.response.values_for(item['SURVEY_MONKEY']), item['SURVEY_MONKEY'], item['TRANSPARENT_CLASSROOM'], item['VALIDATOR'])
                    else:
                        for key in item:
                            if type(item[key]) == dict:
                                self.answers_factory(item[key]) IF ONE, IF ARRAY
                                setattr(self, key.lower(), AND HERE)
                            elsif type(item[key]) == list:
                                # create class with correct capitalization of name
                                # add instance of that class to this
                elsif type(item) == list:
                    HERE






# if creating class, downcase



            else:
                for key in item:
                    self.set_attributes(item[key])
        elif type(item) == list:
            for i in item:
                self.set_attributes(i)
        return all





        @property
        def answers(self):
            return SurveyMonkey.Response.Answers(app.config['HUBS'][response.hub.upper()]['ANSWER_KEY'])






class TransparentClassroom(object):
    def __init__(self, school):
        self.hub = school.hub.upper()
        self.base_url = "{0}/api/v1".format(app.config['TRANSPARENT_CLASSROOM_BASE_URL'])
        self.request_session = requests.session()
        self.request_session.headers.update({
          "X-TransparentClassroomToken": app.config['HUBS'][self.hub]['TRANSPARENT_CLASSROOM_API_TOKEN'],
          "Accept": "application/json",
          "Content-Type": "application/json",
          "X-TransparentClassroomSchoolId": "{0}".format(school.tc_school_id) # for testing and development
        })
        self.school = school


    def submit_application(self, response):
        fields = {
            "session_id": self.school.tc_session_id,
            "program": "Default"
        }
        for item in self.params_key(app.config['HUBS'][self.hub]['ANSWER_KEY'], []):
            print item
            answer = response.answer_for(item['SURVEY_MONKEY'])
            if answer:
                if 'VALIDATOR' in item:
                    if item['VALIDATOR'](answer):
                        fields[item['TRANSPARENT_CLASSROOM']] = answer
                else:
                    fields[item['TRANSPARENT_CLASSROOM']] = answer
        url = "{0}/online_applications.json".format(self.base_url)
        data = json.dumps({"fields": fields})
        print data
        response = self.request_session.post(url, data=data)
        if response.status_code != 201:
            app.logger.error("Posting: {0} To: {1} Response: Status code: {2} Headers: {3} Content: {4}".format(data, url, response.status_code, response.headers, response.content))
            raise LookupError, response
