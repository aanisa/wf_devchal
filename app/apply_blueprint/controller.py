from flask import Blueprint, render_template, request
import models
from app import app, db
import os
from flask_restful import Resource, Api
from flask_cors import cross_origin

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.route('/redirect_to_survey_monkey_with_guid')
def redirect_to_survey_monkey_with_guid():
    return render_template('redirect_to_survey_monkey_with_guid.html', survey_monkey_collector_id=app.config['SURVEY_MONKEY_COLLECTOR_ID'])

@blueprint.route('/after_survey_monkey')
def after_survey_monkey():
    response = models.Response(guid=request.args.get("response_guid"))
    response.email_response()
    for checklist in response.create_checklists():
        checklist.email_checklist()
    return render_template('after_survey_monkey.html')

@blueprint.route('/calendly_webhook', methods=['POST'])
def calendly_webhook():
    models.Appointment(request.get_json()).update_checklist()
    return "OK"
