CREATE ROLE wf;
ALTER ROLE wf WITH LOGIN;

CREATE TABLE "apply_blueprint_school" (
    "id" serial primary key,
    "tc_school_id" INT,
    "tc_session_id" INT,
    "name" TEXT ,
    "match" TEXT ,
    "schedule_parent_teacher_conversation_url" TEXT,
    "schedule_parent_observation_url" TEXT ,
    "email" TEXT,
    "hub" TEXT,
    "email_parent_template" TEXT
);


COPY apply_blueprint_school FROM '/Users/[device User]/Path To/Repo/app/apply_blueprint/seeds/School.development.csv' DELIMITER ',' CSV HEADER;

ALTER TABLE apply_blueprint_school ADD date_created date;
ALTER TABLE apply_blueprint_school ADD date_modified date;

-- Only include this is receive 403 (forbidden) & permission denied to relation apply_blueprint_school
GRANT ALL PRIVILEGES ON TABLE apply_blueprint_school TO wf;
