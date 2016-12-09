from app import app, db
import os
import csv
import models
import ast
import click

path = os.path.dirname(os.path.realpath(__file__))
name = path.split("/")[-1]

@app.cli.group(name = name)
def cli():
    """Namespace for blueprint"""
    pass

@app.cli.command("seed")
@click.pass_context
def seed(ctx):
    """Seed all"""
    ctx.forward(seed_schools)
cli.add_command(seed)

@app.cli.command("seed_schools")
def seed_schools():
    """Seed schools"""
    with open("{0}/seeds/schools.csv".format(path), 'rb') as f:
        schools = []
        for d in csv.DictReader(f):
            school = populate(models.School(), d)
            school.survey_monkey_choice_id=models.Survey().survey_monkey_choice_id_for_school(school)
            schools.append(school)
        db.session.add_all(schools)
        db.session.commit()
    click.echo("Seeded schools")
cli.add_command(seed_schools)

def populate(model, dict):
    for k in dict.keys():
        setattr(model, k, ast.literal_eval("\"{0}\"".format(dict[k])))
    return model
