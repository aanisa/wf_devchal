from app import app, db
import os
import models
import click
import time
import requests


path = os.path.dirname(os.path.realpath(__file__))
name = path.split("/")[-1]

@app.cli.group(name = name)
def cli():
    """Namespace for blueprint"""
    pass

@app.cli.command("seed_from_slack")
def seed_from_slack():
    """Seed from Slack"""

    list_request = requests.get("https://slack.com/api/users.list?token={0}".format(app.config['SLACK_TOKEN']));
    for member in list_request.json()['members']:
        time.sleep(2); # Slack rate limited 
        profile_request = requests.get("https://slack.com/api/users.profile.get?usxer={0}&token={1}&include_labels=true".format(member['id'], app.config['SLACK_TOKEN']));
        print profile_request.text
        profile = profile_request.json()["profile"]
        if profile["fields"]["Xf4XRDP22E"] == "Yes":
            db.session.add(
                models.PublicProfile(
                    slack_id = member['id'],
                    name = profile["real_name"],
                    role = profile["title"],
                    img_url = profile["image_512"],
                    link_url = profile["fields"]["Xf4XSVFQ1K"]["value"],
                    link_text = profile["fields"]["Xf4XSVFQ1K"]["alt"]
                )
            )
    db.session.commit()
cli.add_command(seed_from_slack)
