from flask import Blueprint, render_template, url_for, request, session, redirect
from app import app
import os
import models
from flask_oauthlib.client import OAuth # qbo
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials # gsuite
import json

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

# QBO

qbo = OAuth().remote_app(
    'qbo',
    request_token_url = 'https://oauth.intuit.com/oauth/v1/get_request_token',
    access_token_url  = 'https://oauth.intuit.com/oauth/v1/get_access_token',
    authorize_url     = 'https://appcenter.intuit.com/Connect/Begin',
    consumer_key      = app.config['QBO_CONSUMER_KEY'],
    consumer_secret   = app.config['QBO_CONSUMER_SECRET']
)

@blueprint.route("/authorize_qbo")
def authorize():
    return qbo.authorize(callback=url_for("qbo_authorized"))

@blueprint.route("/qbo_authorized")
def authorized():
    tokens = qbo.authorized_response()
    if tokens is None:
        return "Denied"
    else:
        session['qbo_token'] = tokens
        models.store_authentication_tokens(tokens, request.args.get('realmId'))
    return redirect(url_for("charts_of_accounts"))

@qbo.tokengetter
def tokengetter():
    return session['qbo_token']['oauth_token'], session['qbo_token']['oauth_token_secret']

# GSuite

def flow():
    return OAuth2WebServerFlow(
        client_id=app.config['GSUITE_CLIENT_ID'],
        client_secret=app.config['GSUITE_CLIENT_SECRET'],
        scope='https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/spreadsheets.readonly',
        redirect_uri=url_for("gsuite_authorized", _external=True)
    )

@blueprint.route("/authorize_gsuite")
def authorize_gsuite():
    print url_for("gsuite_authorized")
    return redirect(flow().step1_get_authorize_url())

@blueprint.route("/gsuite_authorized")
def gsuite_authorized():
    credentials = flow().step2_exchange(request.args.get('code'))
    session['gsuite_credentials'] = credentials.to_json()
    return redirect(url_for("charts_of_accounts"))

# Chart of accounts

prefix = "charts_of_accounts/"
@blueprint.route("/{0}".format(prefix), defaults={'path': ""})
@blueprint.route("/{0}<path:path>".format(prefix))
def charts_of_accounts(path):
    credentials = OAuth2Credentials.from_json(session['gsuite_credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('authorize_gsuite'))
    else:
        models.charts_of_accounts(credentials, path)
    # return render_template('charts_of_accounts.html', objects = models.charts_of_accounts("{0}{1}".format(prefix, path)))
