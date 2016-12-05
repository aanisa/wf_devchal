from flask import Blueprint, render_template
import models

apply_blueprint = Blueprint('apply_blueprint', __name__, template_folder='templates')

@apply_blueprint.route('/redirect_to_survey_monkey_with_guid')
def redirect_to_survey_monkey_with_guid():
    return render_template('redirect_to_survey_monkey_with_guid.html', survey_monkey_collector_id=apply_blueprint.config['SURVEY_MONKEY_COLLECTOR_ID'])

@apply_blueprint.route('/after_survey_monkey')
def after_survey_monkey():
    pass
