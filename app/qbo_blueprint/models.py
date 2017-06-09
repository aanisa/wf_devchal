# -*- coding: utf-8 -*-

from app import app, db
import boto3
import os

tablename_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class AuthenticationTokens(Base):
    __tablename__ = "{0}_authentication_tokens".format(tablename_prefix)
    company_id = db.Column(db.BigInteger)
    oauth_token = db.Column(db.String(120))
    oauth_token_secret = db.Column(db.String(120))

def store_authentication_tokens(tokens, company_id):
    authorization_tokens = AuthenticationTokens.query.filter_by(company_id=company_id).first()
    if authorization_tokens is None:
        authorization_tokens = AuthenticationTokens(company_id=company_id)
    authorization_tokens.oauth_token = tokens['oauth_token']
    authorization_tokens.oauth_token_secret = tokens['oauth_token_secret']
    db.session.add(authorization_tokens)
    db.session.commit()

def charts_of_accounts(path):
    bucket = boto3.resource('s3').Bucket(app.config['QBO_S3_BUCKET'])
    result = bucket.meta.client.list_objects(Bucket=bucket.name, Prefix=path, Delimiter="/")
    objects = {}
    for o in result.get("CommonPrefixes", {}):
        objects[o.get("Prefix").split('/')[-2] + "/"] = u'📁'
    for o in result.get("Contents", {}):
        if o.get("Key") != path:
            objects[o.get("Key").split('/')[-1]] = u'🌱'
    return objects
