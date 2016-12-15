from flask import Blueprint, render_template, request
import models
from app import app
import os

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates')

@blueprint.route('/redirect_to_survey_monkey_with_guid')
def redirect_to_survey_monkey_with_guid():
    return render_template('redirect_to_survey_monkey_with_guid.html', survey_monkey_collector_id=app.config['SURVEY_MONKEY_COLLECTOR_ID'])

@blueprint.route('/after_survey_monkey')
def after_survey_monkey():
    checklists = models.Response.create_checklists(request.args.get("guid"))
    for checklist in checklist:
        checklist.email_checklist()
    return render_template('after_survey_monkey.html')

@blueprint.route('/calendly_webhook', methods=['POST'])
def calendly_webhook():
    models.Appointment(request.get_json()).update_checklist()
    return "OK"

@blueprint.route('/completed')
def completed():
    models.Checklist().query.filter(models.Checklist.id == request.args.get("id")).filter(models.Checklist.guid == request.args.get("guid")).first().completed(request.args.get("appointment"))
    return render_template('completed.html')

@blueprint.route('/dashboard')
def dashboard():
    school = models.School.query.get(request.args.get("id"))
    return render_template('dashboard.html', school=school)
