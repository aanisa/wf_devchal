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

class SurveyMonkey:
    request_session = requests.session()
    request_session.headers.update({
      "Authorization": "Bearer {0}".format(app.config['SURVEY_MONKEY_OAUTH_TOKEN']),
      "Content-Type": "application/json"
    })

    class Survey():
        @lru_cache(maxsize=None)
        def __init__(self):
            self.data = request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/details".format(app.config['SURVEY_MONKEY_SURVEY_ID'])).json()

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

        class Question(object):
         def __init__(self, id, text):
             self.id = id
             self.text = text

        @property
        def pages(self):
            pages = []
            for p in self.data["pages"]:
                page = Survey.Page(p["title"])
                for question in p["questions"]:
                    page.questions.append(Survey.Question(question["id"], question["headings"][0]["heading"]))
                pages.append(page)
            return pages

    @lru_cache(maxsize=None)
    def responses(page):
        return request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/responses/bulk".format(app.config["SURVEY_MONKEY_SURVEY_ID"]), params={"sort_order": "DESC", "page": page}).json()

    class Response():
        def __init__(self, guid=None, email=None):
            for i in range(1, 100):
                for d in responses(i)["data"]:
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

        @property
        def as_text(self):
            text = u""
            for page in Survey().pages:
                text = text + u"== {0} ==\n\n".format(page.title)
                for question in page.questions:
                    text = text + u"{0}\n{1}\n\n".format(question.text, u"\n".join(self.answers_for(question.id)))
            return text

        def email_next_steps(self):
            mail.send(
                Message(
                    "Next steps for your application to {0}".format(self.school.name),
                    sender = self.school.emails[0].address,
                    recipients = ["{0} {1} <{2}>".format(
                        Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['FIRST_NAME']['SURVEY_MONKEY']),
                        Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['LAST_NAME']['SURVEY_MONKEY']),
                        Response(guid=self.guid).answer_for(app.config['ANSWER_KEY']['PARENTS'][0]['EMAIL']['SURVEY_MONKEY'])
                    )],
                    body = render_template("email_checklist.txt", school=self.school)
                )
            )

        def email_response(self):
            text = self.as_text
            for school in self.schools:
                for email in school.emails:
                    mail.send(
                        Message(
                            "Application for {0} {1}".format(self.answer_for(app.config['ANSWER_KEY']['CHILD']['FIRST_NAME']['SURVEY_MONKEY']), self.answer_for(app.config['ANSWER_KEY']['CHILD']['LAST_NAME']['SURVEY_MONKEY'])),
                            sender = "Wildflower <noreply@wildflowerschools.org>",
                            recipients = [email.address],
                            body = text
                        )
                    )

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
                return re.sub('<[^<]+?>', '', Survey().value_for(question_id, answer["choice_id"]))
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

        @combomethod
        def create_checklists(receiver, guid=None):
            if inspect.isclass(receiver):
                Response(guid=guid).create_checklists()
            else:
                checklists = []
                for school in receiver.schools:
                    checklists.append(Checklist(guid=receiver.guid, school=school, status="New Application"))
                db.session.add_all(checklists)
                db.session.commit()
                return checklists

class TransparentClassroom(object):
    def __init__(self, tc_school_id):
        self.base_url = "{0}/api/v1".format(app.config["TC_BASE_URL"])
        self.request_session = requests.session()
        self.request_session.headers.update({
          "X-TransparentClassroomToken": app.config['TC_API_TOKEN'],
          "Accept": "application/json",
          "Content-Type": "application/json",
          "X-TransparentClassroomMasqueradeId": "2"
        })
        self.tc_school_id = tc_school_id

    def params_key(self, item, all):
        if type(item) == dict:
            if "TC" in item:
                all.append(item)
            else:
                for key in item:
                    all = self.params_key(item[key], all)
        elif type(item) == list:
            for i in item:
                all = self.params_key(i, all)
        return all

    def submit_application(self, response, program):
        tc_params = {
            "session_id": School.query.filter_by(tc_school_id=self.tc_school_id).first().tc_session_id,
            "program": program
        }
        for item in self.params_key(app.config['ANSWER_KEY'], []):
            tc_params[item['TRANSPARENT_CLASSROOM']] = response.answer_for(item['SURVEY_MONKEY'])
        response = self.request_session.post("{0}/online_applications.json".format(self.base_url), data=json.dumps({"fields": tc_params}))
        if response.status_code != 201:
            raise LookupError, response.body
        return response.json()['data']['id']
