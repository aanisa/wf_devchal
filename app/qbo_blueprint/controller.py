from flask import Blueprint, render_template, url_for, request, session, redirect
from app import app
import os
import models
from flask_oauthlib.client import OAuth

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

qbo = OAuth().remote_app(
    'qbo',
    request_token_url = 'https://oauth.intuit.com/oauth/v1/get_request_token',
    access_token_url  = 'https://oauth.intuit.com/oauth/v1/get_access_token',
    authorize_url     = 'https://appcenter.intuit.com/Connect/Begin',
    consumer_key      = app.config['QBO_CONSUMER_KEY'],
    consumer_secret   = app.config['QBO_CONSUMER_SECRET']
)

@blueprint.route("/authorize")
def authorize():
    return qbo.authorize(callback=url_for("{0}.authorized".format(blueprint.name)))

@blueprint.route("/authorized")
def authorized():
    tokens = qbo.authorized_response()
    if tokens is None:
        return "Denied"
    else:
        session['tokens'] = tokens
        models.store_authentication_tokens(tokens, request.args.get('realmId'))
    return redirect(url_for("{0}.charts_of_accounts".format(blueprint.name)))

@qbo.tokengetter
def tokengetter():
    return session['tokens']['oauth_token'], session['tokens']['oauth_token_secret']

prefix = "charts_of_accounts/"
@blueprint.route("/{0}".format(prefix), defaults={'path': ""})
@blueprint.route("/{0}<path:path>".format(prefix))
def charts_of_accounts(path):
    if path[-5:] == ".json":
        models.set_chart_of_accounts(path)
        return render_template('chart_of_accounts_set.html')
    else:
        return render_template('charts_of_accounts.html', objects = models.charts_of_accounts("{0}{1}".format(prefix, path)))
