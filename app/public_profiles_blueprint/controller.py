from flask import Blueprint, Response, request
from app import app
import models
import os
from flask_cors import CORS, cross_origin

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')
CORS(blueprint)

@blueprint.route('/')
def index():
    return models.PublicProfileSchema(many=True).jsonify(models.PublicProfile.query.order_by(models.PublicProfile.name).all())

@blueprint.route('/slack_event', methods=['POST'])
def slack_event():
    post = request.get_json()
    if post['token'] == app.config['SLACK_VERIFICATION_TOKEN']:
        # for verification - see https://api.slack.com/events/url_verification -> return post['challenge']
        models.PublicProfile.update_profile_from_slack_event(post['event']['user'])
    return "Ok"
