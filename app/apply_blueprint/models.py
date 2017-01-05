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

class EmailSchool(Base):
    __tablename__ = "{0}_email_school".format(tablename_prefix)
    email_id = db.Column('email_id', db.Integer, db.ForeignKey("{0}_email.id".format(tablename_prefix)))
    school_id = db.Column('school_id', db.Integer, db.ForeignKey("{0}_school.id".format(tablename_prefix)))
    school = db.relationship('School', back_populates='emails')
    email = db.relationship('Email', back_populates='schools')

class Email(Base):
    __tablename__ = "{0}_email".format(tablename_prefix)
    address = db.Column(db.String(80))
    schools = db.relationship('EmailSchool', back_populates="email")

class School(Base):
    __tablename__ = "{0}_school".format(tablename_prefix)
    tc_school_id = db.Column(db.Integer)
    checklists = db.relationship('Checklist', backref='school', lazy='dynamic')
    name = db.Column(db.String(80))
    match = db.Column(db.String(80))
    schedule_parent_teacher_conversation_url = db.Column(db.String(80))
    parent_teacher_conversation_optional = db.Column(db.Boolean())
    schedule_parent_observation_url = db.Column(db.String(80))
    parent_observation_optional = db.Column(db.Boolean())
    schedule_child_visit_url = db.Column(db.String(80))
    child_visit_optional = db.Column(db.Boolean())
    emails = db.relationship('EmailSchool', back_populates="school")
    foo = db.relationship('Email', secondary="apply_blueprint_email_school")

request_session = requests.session()
request_session.headers.update({
  "Authorization": "Bearer {0}".format(app.config['SURVEY_MONKEY_OAUTH_TOKEN']),
  "Content-Type": "application/json"
})

class Checklist(Base):
    __tablename__ = "{0}_checklist".format(tablename_prefix)
    guid = db.Column(db.String(36)) # used to link to Survey Monkey results
    school_id = db.Column(db.Integer, db.ForeignKey(School.id))
    parent_teacher_conversation_scheduled_at = db.Column(db.DateTime)
    parent_observation_scheduled_at = db.Column(db.DateTime)
    child_visit_scheduled_at = db.Column(db.DateTime)

    def email_checklist(self):
        mail.send(
            Message(
                "Next steps for your application to {0}".format(self.school.name),
                sender = self.school.email,
                recipients = ["{0} {1} <{2}>".format(
                    Response(guid=self.guid).answer_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0]['FIRST_NAME']),
                    Response(guid=self.guid).answer_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0]['LAST_NAME']),
                    Response(guid=self.guid).answer_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0]['EMAIL'])
                )],
                body = render_template("email_checklist.txt", school=self.school)
            )
        )

    def completed(self, appointment):
        setattr(self, "{0}_scheduled_at".format(appointment), db.func.current_timestamp())
        db.session.commit()

    def response(self):
        return Response(guid=self.guid)

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
                            if question["id"] in [app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0]['EMAIL'], app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][1]['EMAIL']]:
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

    def email_response(self):
        text = self.as_text
        for school in self.schools:
            mail.send(
                Message(
                    "Application for {0} {1}".format(self.answer_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['CHILD']['FIRST_NAME']), self.answer_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['CHILD']['LAST_NAME'])),
                    sender = "Wildflower <noreply@wildflowerschools.org>",
                    recipients = [school.email],
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
        for answer in self.answers_for(app.config['SURVEY_MONKEY_ANSWER_KEY']['SCHOOLS']):
            for school in School.query.all():
                if answer.lower().find(school.match.lower()) >= 0:
                    schools.append(school)
        return schools

    def model_factory(self, class_name, d):
        class ModelFromFactory(): pass
        ModelFromFactory.__name__ = class_name
        m = ModelFromFactory()
        for k in d:
            setattr(m, k.lower(), self.answer_for(d[k]))
        return m

    @property
    def parents(self):
        return [
            self.model_factory("Parent", app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0]),
            self.model_factory("Parent", app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][1])
        ]

    @property
    def child(self):
        return self.model_factory("Child", app.config['SURVEY_MONKEY_ANSWER_KEY']['CHILD'])

    @combomethod
    def create_checklists(receiver, guid=None):
        if inspect.isclass(receiver):
            Response(guid=guid).create_checklists()
        else:
            checklists = []
            for school in receiver.schools:
                checklists.append(Checklist(guid=receiver.guid, school=school))
            db.session.add_all(checklists)
            db.session.commit()
            return checklists

class Appointment():
    def __init__(self, data):
        self.data = data

    @property
    def is_canceled(self):
        return True if self.data["event"] == "invitee.canceled" else False

    @property
    def type(self):
        for t in ["conversation", "observation", "visit"]:
            if self.data["payload"]["event_type"]["slug"].find(t) >= 0:
                return t
        raise LookupError

    @property
    def school(self):
        return School.query.filter(School.email == self.data["payload"]["event"]["extended_assigned_to"][0]["email"]).first()

    @property
    def response(self):
        return Response(email=self.data["payload"]["invitee"]["email"])

    @property
    def at(self):
        return dateutil.parser.parse(self.data["payload"]["event"]["start_time"])

    @property
    def checklist(self):
        return Checklist.query.filter(Checklist.guid == self.response.guid, Checklist.school == self.school).first()

    @combomethod
    def update_checklist(receiver, data=None):
        if inspect.isclass(receiver):
            Appointment(data).update_checklist();
        else:
            setattr(receiver.checklist, "{0}_scheduled_at".format(receiver.type), None if receiver.is_canceled else receiver.at)
            db.session.commit()

def schema_factory(name, fields):
    class SchemaFromFactory(ma.Schema):
        class Meta: pass
        Meta.fields = fields
    SchemaFromFactory.__name__ = "{0}Schema".format(name)
    return SchemaFromFactory()

class ResponseSchema(ma.Schema):
    guid = ma.String()
    child = ma.Nested(schema_factory("Child", [k.lower() for k in app.config['SURVEY_MONKEY_ANSWER_KEY']['CHILD'].keys()]))
    parents = ma.Nested(schema_factory("Parent", [k.lower() for k in app.config['SURVEY_MONKEY_ANSWER_KEY']['PARENTS'][0].keys()]), many=True)

class ChecklistSchema(ma.ModelSchema):
    class Meta:
        model = Checklist
    response = ma.Nested(ResponseSchema)

class SchoolSchema(ma.ModelSchema):
    class Meta:
        model = School
    checklists = ma.Nested(ChecklistSchema, many=True)
