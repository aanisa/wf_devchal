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
def seed():
    """Seed"""
    seeds = []
    for f in [f for f in os.listdir("{0}/seeds/".format(path))]:
        model_name = f.split(".")[0]
        with open("{0}/seeds/{1}".format(path, f), 'rb') as f:
            click.echo("Seeding {0}".format(model_name))
            for d in csv.DictReader(f):
                seeds.append(populate(eval("models.{0}()".format(model_name)), d))
    db.session.add_all(seeds)
    db.session.commit()
cli.add_command(seed)

def populate(seed, dict):
    for k in dict.keys():
        setattr(seed, k, ast.literal_eval("\"{0}\"".format(dict[k])))
    return seed
