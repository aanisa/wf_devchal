# -*- coding: utf-8 -*-

import boto3
from app import app
from flask_oauthlib.client import OAuth

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

oauth = OAuth()
qbo = oauth.remote_app(
    'qbo',
    request_token_url = 'https://oauth.intuit.com/oauth/v1/get_request_token',
    access_token_url  = 'https://oauth.intuit.com/oauth/v1/get_access_token',
    authorize_url     = 'https://appcenter.intuit.com/Connect/Begin',
    consumer_key      = app.config['QBO_CONSUMER_KEY'],
    consumer_secret   = app.config['QBO_CONSUMER_SECRET']
)

@qbo.tokengetter
def get_qbo_token():
    # return resp['oauth_token'], resp['oauth_token_secret']
    print "get_qbo_token"

def store_credentials(resp, realm_id):
    # if realm_id is already there then delete

    # insert
