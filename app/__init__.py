from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

for f in [f for f in os.listdir(os.path.dirname(os.path.realpath(__file__)))]:
    if f.find("_blueprint") >= 0:
        p = f[0:-10] # _blueprint is 10 chars long
        print "Registering blueprint {0} at {1}".format(p, f)
        # exec("from {0}.controller import blueprint".format(f))
        exec("from {0}.controller import blueprint".format(f))
        eval("app.register_blueprint(blueprint, url_prefix='/{1}')".format(f, p))
