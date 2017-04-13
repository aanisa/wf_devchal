from flask import Blueprint, Response, request
from app import app
import models
import os

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.route('/')
def index():
    return models.PublicProfileSchema(many=True).jsonify(models.PublicProfile.query.all())

@blueprint.route('/slack_event')
def slack_event():
    post = request.get_json()
    app.logger.critical(post[challenge])
    if post['token'] == app.config['SLACK_TOKEN']:
        # for verification - see https://api.slack.com/events/url_verification
        return post['challenge']
