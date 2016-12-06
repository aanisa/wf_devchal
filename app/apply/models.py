from app import app, db
import sqlalchemy.orm
from functools32 import lru_cache
import datetime
import requests

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

    def create_checklists(self):
        for school in self.schools():
            school.checklists.append(Checklist(guid=self.guid))
        db.session.commit()

class Appointment():
    def __init__(self, data):
        self.data = data

    @property
    def is_cancelled(self):
        if self.data["event"] == "invitee.canceled":
            return True
        return False

    @property
    def is_created(self):
        if self.data["event"] == "invitee.created":
            return True
        return False

    @property
    def is_interview(self):
        raise

    @property
    def is_observation(self):
        raise

    @property
    def school(self):
        return School.query.filter(School.email == self.data["payload"]["event"]["extended_assigned_to"]["email"]).first()

    @property
    def response(self):
        raise

    @property
    def at(self):
        raise

    def checklist(self):
        raise

    def update_checklist(self):
        c = self.checklist
        if self.is_interview:
            if self.is_cancelled:
                c.interview_scheduled_at = None
            else if self.is_created:
                c.interview_scheduled_at = self.at
            else:
                raise LookupError
        else if self.is_observation
            if self.is_cancelled:
                c.observation_scheduled_at = None
            else if self.is_created:
                c.observation_scheduled_at = self.at
            else:
                raise LookupError
        else:
            raise LookupError
        db.session.commit()
