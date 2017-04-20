from app import app, db
import os
import models

path = os.path.dirname(os.path.realpath(__file__))
name = path.split("/")[-1]

@app.cli.group(name = name)
def cli():
    """commands for blueprint"""
    pass

@cli.command("seed_from_slack")
def seed_from_slack():
    """Seed from Slack"""
    models.PublicProfile.seed_from_slack()
cli.add_command(seed_from_slack)
