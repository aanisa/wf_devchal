from app import app, db, mail
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

table_name_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Checklist(Base):
    __tablename__ = "{0}_checklist".format(table_name_prefix)
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36)) # used to link to Survey Monkey results
    school_id = db.Column(db.Integer, db.ForeignKey("{0}_school.id".format(table_name_prefix)))
    school = sqlalchemy.orm.relationship("School", back_populates="checklists")
    interview_scheduled_at = db.Column(db.DateTime)
    observation_scheduled_at = db.Column(db.DateTime)
    visit_scheduled_at = db.Column(db.DateTime)

    def email_checklist(self):
        mail.send(
            Message(
                "Next steps for your application to {0}".format(self.school.name),
                sender = self.school.email,
                recipients = [Response(guid=self.guid).answer_for(app.config['SURVEY_MONKEY_EMAIL_QUESTION_IDS'][0])],
                body = render_template("email_checklist.txt", school=self.school)
            )
        )

    def completed(self, appointment):
        setattr(self, "{0}_scheduled_at".format(appointment), db.func.current_timestamp())
        db.session.commit()

class School(Base):
    __tablename__ = "{0}_school".format(table_name_prefix)
    id = db.Column(db.Integer, primary_key=True)
    checklists = sqlalchemy.orm.relationship("Checklist", back_populates="school")
    name = db.Column(db.String(80))
    match = db.Column(db.String(80))
    interview_optional = db.Column(db.Boolean())
    schedule_interview_url = db.Column(db.String(80))
    schedule_observation_url = db.Column(db.String(80))
    observation_optional = db.Column(db.Boolean())
    schedule_visit_url = db.Column(db.String(80))
    visit_optional = db.Column(db.Boolean())
    email = db.Column(db.String(80))

request_session = requests.session()
request_session.headers.update({
  "Authorization": "Bearer {0}".format(app.config['SURVEY_MONKEY_OAUTH_TOKEN']),
  "Content-Type": "application/json"
})

class Survey():
    @lru_cache(maxsize=None)
    def __init__(self):
        self.data = request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/details".format(app.config['SURVEY_MONKEY_SURVEY_ID'])).json()

    def school_for(self, survey_monkey_choice_id):
        for page in self.data["pages"]:
            for question in page["questions"]:
                if question["id"] == app.config['SURVEY_MONKEY_WHICH_SCHOOLS_QUESTION_ID']:
                    for choice in question["answers"]["choices"]:
                        if choice["id"] == survey_monkey_choice_id:
                            for school in School.query.all():
                                if choice["text"].lower().find(school.match.lower()) >= 0:
                                    return school
        raise LookupError

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
                            if question["id"] in app.config['SURVEY_MONKEY_EMAIL_QUESTION_IDS']:
                                if question["answers"][0]["text"].lower() == email.lower():
                                    self.data = d
                                    return
        raise LookupError

    def answer_for(self, question_id):
        for page in self.data["pages"]:
            for question in page["questions"]:
                if question["id"] == question_id:
                    return question["answers"][0]["text"]
                    # this only works for simple, single answer, text answers
                    # will have to be updated later for less simple answers
        raise LookupError

    @property
    def schools(self):
        schools = []
        for page in self.data["pages"]:
            for question in page["questions"]:
                if question["id"] == app.config['SURVEY_MONKEY_WHICH_SCHOOLS_QUESTION_ID']:
                    for answer in question["answers"]:
                        schools.append(Survey().school_for(answer["choice_id"]))
        return schools

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
        for t in ["interview", "observation", "visit"]:
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
