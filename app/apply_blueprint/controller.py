from flask import Blueprint, render_template, request
import models
from app import app, db
import os
from flask_mail import Message
import traceback

app.jinja_env.add_extension('jinja2.ext.do')
blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.errorhandler(500)
def five_hundred(e):
    models.mail.send(
        Message(
            "500 - URL: {0} Error: {1}".format(request.url, e),
            sender="Wildflower Schools <noreply@wildflowerschools.org>",
            recipients=['dan.grigsby@wildflowerschools.org'],
            body=traceback.format_exc()
        )
    )
    return render_template('500.html')

@blueprint.route('/redirect_to_survey_monkey_with_guid')
def redirect_to_survey_monkey_with_guid():
    hub = request.args.get("hub")
    return render_template('redirect_to_survey_monkey_with_guid.html', hub=hub, SURVEY_MONKEY_COLLECTOR_ID=app.config['HUBS'][hub.upper()]['SURVEY_MONKEY_COLLECTOR_ID'])

@blueprint.route('/after_survey_monkey')
def after_survey_monkey():
    response = models.SurveyMonkey.Response(request.args.get("hub"), guid=request.args.get("response_guid"))
    application = models.Application(response)
    application.submit_to_transparent_classroom()
    application.email_schools()
    application.email_parent()
    return render_template('after_survey_monkey.html', application=application)
