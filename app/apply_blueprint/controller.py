from flask import Blueprint, render_template, request, redirect, jsonify
import models
from app import app, db
import os
from flask_mail import Message
import traceback
from flask_cors import CORS, cross_origin

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

app.jinja_env.add_extension('jinja2.ext.do')

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

@blueprint.route('/email_template')
@cross_origin()
def email_template():
    # TODO authenticate request; take token as param and use TC API
    tc_school_id = request.args.get("tc_school_id")
    school = models.School.query.filter_by(tc_school_id=tc_school_id).first()
    return redirect(school.email_template_get_url())

@blueprint.route('/email_template_post_parameters')
@cross_origin()
def email_template_post_parameters():
    # TODO authenticate request; take token as param and use TC API
    tc_school_id = request.args.get("tc_school_id")
    school = models.School.query.filter_by(tc_school_id=tc_school_id).first()
    return jsonify(school.email_template_post_parameters())

# curl \
# -v \
# -F "key=email-templates/cambridge/Aster Montessori School.html" \
# -F "policy=eyJjb25kaXRpb25zIjogW3siYnVja2V0IjogIndmLWFwcGxpY2F0aW9uLXV0aWxpdHkifSwgeyJrZXkiOiAiZW1haWwtdGVtcGxhdGVzL2NhbWJyaWRnZS9Bc3RlciBNb250ZXNzb3JpIFNjaG9vbC5odG1sIn0sIHsieC1hbXotYWxnb3JpdGhtIjogIkFXUzQtSE1BQy1TSEEyNTYifSwgeyJ4LWFtei1jcmVkZW50aWFsIjogIkFLSUFJSkVXTko2T0pQQ0ZRQ09BLzIwMTcwNTA1L3VzLWVhc3QtMS9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMTcwNTA1VDE5MDk1N1oifV0sICJleHBpcmF0aW9uIjogIjIwMTctMDUtMDVUMjA6MDk6NTdaIn0=" \
# -F "x-amz-algorithm=AWS4-HMAC-SHA256" \
# -F "x-amz-credential=AKIAIJEWNJ6OJPCFQCOA/20170505/us-east-1/s3/aws4_request" \
# -F "x-amz-date=20170505T190957Z" \
# -F  "x-amz-signature=4abd7ef930ac7af1c4be4f825fb4a29f0850fb77fe1b59fb1d23da081d5afa1f" \
# -F "file=@template.html" \
# https://wf-application-utility.s3.amazonaws.com/
