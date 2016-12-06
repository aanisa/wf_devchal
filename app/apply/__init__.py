from app import app, db
import os
import csv
import models

path = os.path.dirname(os.path.realpath(__file__))

@app.cli.command("{0}_seed_schools".format(path.split("/")[-1]))
def seed_command():
    with open("{0}/seed_schools.csv".format(path), 'rb') as f:
        schools = []
        for s in csv.DictReader(f):
            school = models.School(name=s["name"], schedule_interview_url=s["schedule_interview_url"], schedule_observation_url=s["schedule_interview_url"], email=s["email"], match=s["match"])
            school.survey_monkey_choice_id=models.Survey().survey_monkey_choice_id_for_school(school)
            schools.append(school)
        db.session.add_all(schools)
        db.session.commit()
