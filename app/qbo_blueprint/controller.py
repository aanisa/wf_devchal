from flask import Blueprint, render_template, url_for, request, session, redirect
from app import app
import os
import models
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials # gsuite
import httplib2
from apiclient import discovery
from flask_oauthlib.client import OAuth # qbo

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.route("/")
def index():
    return redirect(url_for("{0}.authorize_gsuite".format(blueprint.name)))

# Step-1, authorize GSuite

def flow():
    return OAuth2WebServerFlow(
        client_id=app.config['GSUITE_CLIENT_ID'],
        client_secret=app.config['GSUITE_CLIENT_SECRET'],
        scope='https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/spreadsheets.readonly',
        redirect_uri=url_for("{0}.gsuite_authorized".format(blueprint.name), _external=True)
    )

@blueprint.route("/authorize_gsuite")
def authorize_gsuite():
    return redirect(flow().step1_get_authorize_url())

@blueprint.route("/gsuite_authorized")
def gsuite_authorized():
    credentials = flow().step2_exchange(request.args.get('code'))
    session['gsuite_credentials'] = credentials.to_json()
    return redirect(url_for("{0}.charts_of_accounts".format(blueprint.name)))

# Step-2, choose a chart of accounts

prefix = "charts_of_accounts/"
@blueprint.route("/{0}".format(prefix), defaults={'id': app.config['GSUITE_CHARTS_OF_ACCOUNTS_FOLDER_ID']})
@blueprint.route("/{0}<string:id>".format(prefix))
def charts_of_accounts(id):
    credentials = OAuth2Credentials.from_json(session['gsuite_credentials'])
    if credentials.access_token_expired:
        return redirect(url_for("{0}.authorize_gsuite".format(blueprint.name)))
    http_auth = credentials.authorize(httplib2.Http())
    drive = discovery.build('drive', 'v3', http_auth)
    files = drive.files().list(q="'{0}' in parents and (mimeType='application/vnd.google-apps.spreadsheet' or mimeType='application/vnd.google-apps.folder')".format(id), orderBy="name").execute()['files']
    return render_template('charts_of_accounts.html', files = files, blueprint_name = blueprint.name)

@blueprint.route("/set_chart_of_accounts/<string:sheet_id>")
def set_chart_of_accounts(sheet_id):
    session['sheet_id'] = sheet_id
    return redirect(url_for("{0}.authorize_qbo".format(blueprint.name)))

# Step-3, authorize QBO

qbo = OAuth().remote_app(
    'qbo',
    request_token_url = 'https://oauth.intuit.com/oauth/v1/get_request_token',
    access_token_url  = 'https://oauth.intuit.com/oauth/v1/get_access_token',
    authorize_url     = 'https://appcenter.intuit.com/Connect/Begin',
    consumer_key      = app.config['QBO_CONSUMER_KEY'],
    consumer_secret   = app.config['QBO_CONSUMER_SECRET']
)

@blueprint.route("/authorize_qbo")
def authorize_qbo():
    return qbo.authorize(callback=url_for("{0}.qbo_authorized".format(blueprint.name)))

@blueprint.route("/qbo_authorized")
def qbo_authorized():
    qbo_tokens = qbo.authorized_response()
    session['qbo_tokens'] = qbo_tokens;
    models.store_qbo_authentication_tokens(qbo_tokens, request.args.get('realmId'))
    return redirect(url_for("{0}.update_chart_of_accounts".format(blueprint.name)))

@qbo.tokengetter
def tokengetter():
    return session['qbo_tokens']['oauth_token'], session['qbo_tokens']['oauth_token_secret']

# Step-4, update chart of accounts

@blueprint.route("/update_chart_of_accounts")
def update_chart_of_accounts():
    models.update_chart_of_accounts(session['qbo_tokens'], OAuth2Credentials.from_json(session['gsuite_credentials']), session['sheet_id'])
    return render_template('update_chart_of_accounts.html')
