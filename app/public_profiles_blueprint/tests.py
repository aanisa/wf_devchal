import unittest
import models
import flask
from app import app, db
import os

blueprint_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit() # fixes hang - see http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
    
    def test_create(self):
        create_json = """
         {"token":"L09Z6DChuoFeeZ2MN3LOD7mm","team_id":"T1BCRBEKF","api_app_id":"A4XK63K32","event":{"type":"user_change","user":{"id":"U2ZSSJ9B5","team_id":"T1BCRBEKF","name":"testuser","deleted":false,"status":null,"color":"8469bc","real_name":"Test User","tz":"America\/Chicago","tz_label":"Central Daylight Time","tz_offset":-18000,"profile":{"first_name":"Test","last_name":"User","avatar_hash":"gf79c0913b9f","fields":{"Xf4XRDP22E":{"value":"Yes","alt":""}},"real_name":"Test User","real_name_normalized":"Test User","email":"dan.grigsby+slacktmp@wildflowerschools.org","image_24":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-24.png","image_32":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-32.png","image_48":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-48.png","image_72":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-72.png","image_192":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0015-192.png","image_512":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0015-512.png"},"is_admin":false,"is_owner":false,"is_primary_owner":false,"is_restricted":false,"is_ultra_restricted":false,"is_bot":false,"updated":1492101122},"cache_ts":1492101122,"event_ts":"1492101122.776926"},"type":"event_callback","authed_users":["U2ZSSJ9B5"],"event_id":"Ev4ZKH9L3G","event_time":1492101122}
        """

        with app.test_request_context():
            url = flask.url_for("{0}.slack_event".format(blueprint_name))
            response = app.test_client().post(
                url,
                content_type='application/json',
                data=create_json
            )
            self.assertEqual(response.status_code, 200)


    def test_delete(self):
        delete_json = """
        {"token":"L09Z6DChuoFeeZ2MN3LOD7mm","team_id":"T1BCRBEKF","api_app_id":"A4XK63K32","event":{"type":"user_change","user":{"id":"DELETEME","team_id":"T1BCRBEKF","name":"testuser","deleted":true,"profile":{"first_name":"Test","last_name":"User","avatar_hash":"gf79c0913b9f","fields":{"Xf4XRDP22E":{"value":"Yes","alt":""}},"real_name":"Test User","real_name_normalized":"Test User","email":"dan.grigsby+slacktmp@wildflowerschools.org","image_24":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-24.png","image_32":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-32.png","image_48":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-48.png","image_72":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0015-72.png","image_192":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0015-192.png","image_512":"https:\/\/secure.gravatar.com\/avatar\/f79c0913b9f6e6cec5aef3c493fbadc1.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0015-512.png"},"is_bot":false,"updated":1492101122},"cache_ts":1492101278,"event_ts":"1492101277.818222"},"type":"event_callback","authed_users":["U2ZSSJ9B5"],"event_id":"Ev4YSXH8KD","event_time":1492101277}
        """

        profile = models.PublicProfile(slack_id="DELETEME")
        db.session.add(profile)
        db.session.commit()

        self.assertEqual(models.PublicProfile.query.filter_by(slack_id="DELETEME").first(), profile)

        with app.test_request_context():
            url = flask.url_for("{0}.slack_event".format(blueprint_name))
            response = app.test_client().post(
                url,
                content_type='application/json',
                data=delete_json
            )

        self.assertEqual(models.PublicProfile.query.filter_by(slack_id="DELETEME").first(), None)
