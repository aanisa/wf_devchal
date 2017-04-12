from app import app, db, ma
import os
import sqlalchemy.orm
import requests

tablename_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Directory(Base):
    __tablename__ = "{0}_directory".format(tablename_prefix)
    slack_id = db.Column(db.String(120))
    name = db.Column(db.String(120))
    role = db.Column(db.String(120))
    img_url = db.Column(db.String(120))
    link_url = db.Column(db.String(120))
    link_text = db.Column(db.String(120))

class DirectorySchema(ma.ModelSchema):
    class Meta:
        model = Directory
