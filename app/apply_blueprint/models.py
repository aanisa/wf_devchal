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
from nltk.stem import WordNetLemmatizer

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
            response = super(type(self), self).get(url, params=params, **kwargs)
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
                            if question["id"] in [app.config['HUBS'][self.hub.upper()]['MAPPING']['parents'][0]['email']['survey_monkey'], app.config['HUBS'][self.hub.upper()]['MAPPING']['parents'][1]['email']['survey_monkey']]:
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

        class Base(object):
            def __repr__(self):
                from pprint import pformat
                return pformat(vars(self), indent=4, width=1)


        class Answer(Base):
            def __init__(self, value, survey_monkey_question_id, transparent_classroom_key, validator):
                self.value = value
                self.survey_monkey_question_id = survey_monkey_question_id
                self.transparent_classroom_key = transparent_classroom_key
                self.validator = validator

            def __str__(self):
                if type(self.value) == list:
                    return "\n".join(self.value)
                return self.value


        class Answers(Base):
            def __init__(self, response, item):
                self.response = response
                mapping = self.answers_factory(item, "MAPPING")
                for key in mapping.__dict__:
                    setattr(self, key, getattr(mapping, key))

            def snake_case_name(self, name):
                name = name.lower()
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
                return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

            def model_factory(self, key):
                wnl = WordNetLemmatizer()
                lowercase_words = [word.lower() for word in str.split(key)]
                singular_lowercase_words = [wnl.lemmatize(word) for word in lowercase_words ]
                titleize_singular_words = [word.title() for word in singular_lowercase_words]
                class ModelFromFactory(SurveyMonkey.Response.Base): pass
                ModelFromFactory.__name__ = ''.join(titleize_singular_words).encode('ascii', 'ignore')
                return ModelFromFactory()

            def answers_factory(self, item, name):
                if type(item) == dict:
                    if "TRANSPARENT_CLASSROOM" in item:
                        value = self.response.values_for(item['SURVEY_MONKEY'])
                        if len(value) == 0:
                            value = None
                        elif len(value) == 1: # use value, not list, is there's only one
                            value = value[0]
                        return SurveyMonkey.Response.Answer(value, item['SURVEY_MONKEY'], item['TRANSPARENT_CLASSROOM'], item.get('VALIDATOR'))
                    else:
                        # dct = {}
                        model = self.model_factory(name)
                        for key in item:
                            value = self.answers_factory(item[key], key)
                            setattr(model, self.snake_case_name(key), value)
                            # dct[key] = value
                        # return dct
                        return model
                elif type(item) == list:
                    lst = []
                    for list_item in item:
                        lst.append(self.answers_factory(list_item, name))
                    return lst
                else:
                    raise LookupError


        @property
        def answers(self):
            return SurveyMonkey.Response.Answers(self, app.config['HUBS'][self.hub.upper()]['MAPPING'])

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
        for item in self.params_key(app.config['HUBS'][self.hub]['MAPPING'], []):
            answer = response.answer_for(item['SURVEY_MONKEY'])
            if answer:
                if 'VALIDATOR' in item:
                    if item['VALIDATOR'](answer):
                        fields[item['TRANSPARENT_CLASSROOM']] = answer
                else:
                    fields[item['TRANSPARENT_CLASSROOM']] = answer
        url = "{0}/online_applications.json".format(self.base_url)
        data = json.dumps({"fields": fields})
        response = self.request_session.post(url, data=data)
        if response.status_code != 201:
            app.logger.error("Posting: {0} To: {1} Response: Status code: {2} Headers: {3} Content: {4}".format(data, url, response.status_code, response.headers, response.content))
            raise LookupError, response
