from app import app, db, ma
import os
import sqlalchemy.orm
import urllib
import requests
import time

tablename_prefix = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

def slack_api(method, arguments = {}):
    url = "https://slack.com/api/{0}?token={1}&{2}".format(method, app.config['SLACK_TOKEN'], urllib.urlencode(arguments))
    while True:
        response = requests.get(url)
        if response.status_code == 429:
            print "rate limited; sleeping for {0} seconds".format(response.headers[Retry-After])
            time.sleep(float(response.headers[Retry-After]))
        else:
            # print response.text
            return response.json()

class PublicProfile(Base):
    __tablename__ = "{0}_public_profile".format(tablename_prefix)
    slack_id      = db.Column(db.String(120))
    name          = db.Column(db.String(120))
    role          = db.Column(db.String(120))
    img_url       = db.Column(db.String(120))
    link_url      = db.Column(db.String(120))
    link_text     = db.Column(db.String(120))

    @classmethod
    def seed_from_slack(cls):
        user_list = slack_api("users.list")["members"]
        for user in user_list:
            profile = slack_api("users.profile.get", {"user": user['id']})["profile"]
            if profile["fields"] and profile["fields"].get("Xf4XRDP22E",{}).get("value") == "Yes":
                print "adding {0}".format(profile["real_name"])
                db.session.add(
                    PublicProfile(
                        slack_id  = user['id'],
                        name      = profile["real_name"],
                        role      = profile["title"],
                        img_url   = profile["image_512"],
                        link_url  = profile["fields"].get("Xf4XSVFQ1K", {}).get("value"),
                        link_text = profile["fields"].get("Xf4XSVFQ1K", {}).get("alt")
                    )
                )
        db.session.commit()

class PublicProfileSchema(ma.ModelSchema):
    class Meta:
        model = PublicProfile
