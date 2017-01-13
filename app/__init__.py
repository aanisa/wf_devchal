from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_mail import Mail, Message
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

app.config.from_object('config.default')
app.config.from_object("config.{0}".format(os.environ['APP_CONFIG_MODE']))

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

for f in [f for f in os.listdir(os.path.dirname(os.path.realpath(__file__)))]:
    if f.find("_blueprint") >= 0:
        p = f[0:-10] # _blueprint is 10 chars long
        app.logger.info("Registering blueprint {0} at {1}".format(f, p))
        eval("app.config.from_object('app.{0}.config.default')".format(f))
        eval("app.config.from_object('app.{0}.config.{1}')".format(f, os.environ['APP_CONFIG_MODE']))
        exec("from {0}.controller import blueprint".format(f))
        eval("app.register_blueprint(blueprint, url_prefix='/{0}')".format(p))
        exec("import {0}.cli".format(f))
