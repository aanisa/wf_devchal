from app import app, db
import sqlalchemy.orm
from functools32 import lru_cache
import datetime
import requests
from combomethod import combomethod
import inspect
import dateutil.parser

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Checklist(Base):
    __tablename__ = "apply_checklist"
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36)) # used to link to Survey Monkey results
    school_id = db.Column(db.Integer, db.ForeignKey('apply_school.id'))
    school = sqlalchemy.orm.relationship("School", back_populates="checklists")
    interview_scheduled_at = db.Column(db.DateTime)
    observation_scheduled_at = db.Column(db.DateTime)

class School(Base):
    __tablename__ = "apply_school"
    id = db.Column(db.Integer, primary_key=True)
    checklists = sqlalchemy.orm.relationship("Checklist", back_populates="school")
    name = db.Column(db.String(80))
    match = db.Column(db.String(80))
    schedule_interview_url = db.Column(db.String(80))
    schedule_observation_url = db.Column(db.String(80))
    email = db.Column(db.String(80))
    survey_monkey_choice_id = db.Column(db.String(80))

request_session = requests.session()
request_session.headers.update({
  "Authorization": "Bearer {0}".format(app.config['SURVEY_MONKEY_OAUTH_TOKEN']),
  "Content-Type": "application/json"
})

class Survey():
    @lru_cache(maxsize=None)
    def __init__(self):
        self.data = request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/details".format(app.config['SURVEY_MONKEY_SURVEY_ID'])).json()

    def survey_monkey_choice_id_for_school(self, school):
        for page in self.data["pages"]:
            for question in page["questions"]:
                if question["id"] == app.config['SURVEY_MONKEY_WHICH_SCHOOLS_QUESTION_ID']:
                    for choice in question["answers"]["choices"]:
                        if choice["text"].lower().find(school.match.lower()) >= 0:
                            return choice["id"]
        raise LookupError

@lru_cache(maxsize=None)
def responses():
    return request_session.get("https://api.surveymonkey.net/v3/surveys/{0}/responses/bulk".format(app.config["SURVEY_MONKEY_SURVEY_ID"]), params={"sort_order": "DESC"}).json()

class Response():
    def __init__(self, guid):
        self.guid = guid
        for d in responses()["data"]:
            if d["custom_variables"]["response_guid"] == self.guid:
                self.data = d

    @property
    def schools(self):
        schools = []
        for page in self.data["pages"]:
            for question in page["questions"]:
                if question["id"] == app.config['SURVEY_MONKEY_WHICH_SCHOOLS_QUESTION_ID']:
                    for answer in question["answers"]:
                        schools.append(School.query.filter(School.survey_monkey_choice_id == answer["choice_id"]).first())
        return schools

    @combomethod
    def create_checklists(receiver, guid=None):
        if inspect.isclass(receiver):
            Checklist(guid).create_checklists()
        else:
            for school in self.schools():
                school.checklists.append(Checklist(guid=receiver.guid))
            db.session.commit()

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
        return School.query.filter(School.email == self.data["payload"]["event"]["extended_assigned_to"]["email"]).first()

    @property
    def response(self):
        # use invitee's email address to find response - look for either parent
        # will require another setting to find correct place for answer in response
        raise

    @property
    def at(self):
        print dateutil.parser.parse(self.data["payload"]["event"]["start_time"])
        return dateutil.parser.parse(self.data["payload"]["event"]["start_time"])

    def checklist(self):
        return Checklist.query.filter(Checklist.guid == self.response.guid, Checklist.school == self.school).first()

    @combomethod
    def update_checklist(receiver, data=None):
        if inspect.isclass(receiver):
            Appointment(data).update_checklist();
        else:
            setattr(receiver.checklist, "{0}_scheduled_at".format(receiver.type), None if receiver.is_canceled else receiver.at)
            db.session.commit()
