from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from apply.controller import apply_blueprint
app.register_blueprint(apply_blueprint, url_prefix='/apply')
