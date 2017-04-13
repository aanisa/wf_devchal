from app import app, db
import os
import models
import click

path = os.path.dirname(os.path.realpath(__file__))
name = path.split("/")[-1]

@app.cli.group(name = name)
def cli():
    """Namespace for blueprint"""
    pass

@app.cli.command("seed_from_slack")
def seed_from_slack():
    """Seed from Slack"""
    models.PublicProfile.seed_from_slack()
cli.add_command(seed_from_slack)
