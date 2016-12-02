from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)

from apply.controller import apply_blueprint
app.register_blueprint(apply_blueprint, url_prefix='/apply')
