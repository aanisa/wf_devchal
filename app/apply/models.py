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
