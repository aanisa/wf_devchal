from flask import Blueprint, render_template, url_for, request
from app import app
import os
import models

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.route("/authorize")
def authorize():
    return models.qbo.authorize(callback=url_for("{0}.authorized".format(blueprint.name)))

@blueprint.route("/authorized")
def authorized():
    resp = models.qbo.authorized_response()
    if resp is None:
        return "Denied"
    else:
        models.store_credentials(resp, request.args.get('realmId'))
    return redirect(url_for("{0}.charts_of_accounts".format(blueprint.name)))

prefix = "charts_of_accounts/"
@blueprint.route("/{0}".format(prefix), defaults={'path': ""})
@blueprint.route("/{0}<path:path>".format(prefix))
def charts_of_accounts(path):
    return render_template('charts_of_accounts.html', objects = models.charts_of_accounts("{0}{1}".format(prefix, path)))
