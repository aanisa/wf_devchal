from app import app, db
import os
import csv
import models
import ast

path = os.path.dirname(os.path.realpath(__file__))

@app.cli.command("{0}_seed".format(path.split("/")[-1]))
def seed_command():
    seed_schools_command()

@app.cli.command("{0}_seed_schools".format(path.split("/")[-1]))
def seed_schools_command():
    with open("{0}/seed_schools.csv".format(path), 'rb') as f:
        schools = []
        for d in csv.DictReader(f):
            s = populate(School(), d)
            s.survey_monkey_choice_id=models.Survey().survey_monkey_choice_id_for_school(school)
            schools.append(s)
        db.session.add_all(schools)
        db.session.commit()

def populate(model, dict):
    for k in dict.keys():
        setattr(model, k, ast.literal_eval(dict[k]))
