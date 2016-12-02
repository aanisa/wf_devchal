from app import db
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
import datetime

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
    school = relationship("School", back_populates="apply_school")
    interview_scheduled_at = db.Column(db.DateTime)
    observation_scheduled_at = db.Column(db.DateTime)

class School(Base):
    __tablename__ = "apply_school"
    id = db.Column(db.Integer, primary_key=True)
    checklists = relationship("Checklist", back_populates="apply_checklist")
    name = db.Column(db.String(80))
    schedule_interview_url = db.Column(db.String(80))
    schedule_observation_url = db.Column(db.String(80))
    email = db.Column(db.String(80))
    survey_monkey_choice_id = db.Column(db.String(80))
