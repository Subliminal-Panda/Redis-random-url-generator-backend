from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import psycopg2
import os

import random
import string

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://tyiqnhngopukqe:870e05ace212a1cfaaa9e73057d5729f4a9c237e80b77e24ead707a6cbbe78ef@ec2-54-167-152-185.compute-1.amazonaws.com:5432/de30ecaso2mj79"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=False, nullable=False)
    key = db.Column(db.String, nullable=True)



    def __init__(self, id, url, key):
        self.id = id
        self.url = url
        self.key = key

class UrlSchema(ma.Schema):
    class Meta:
        fields = ('id', 'url', 'key')

url_schema = UrlSchema()
multiple_url_schema = UrlSchema(many=True)


@app.route('/url/add', methods=["POST"])
def add_url():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be Formatted as JSON.')

    post_data = request.get_json()
    url = post_data.get('url')
    custom_link = post_data.get('custom link')
    if custom_link == None:
        key = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])
    else:
        key = custom_link

    new_url = Url(id, url, key)

    db.session.add(new_url)
    db.session.commit()
    successful = ["New URL added to database:", url_schema.dump(new_url)]
    return jsonify(successful)

@app.route('/url/get', methods=["GET"])
def get_all_keys():
    all_keys = redis_client.keys("*")
    return jsonify([key.decode('utf-8') for key in all_keys])

@app.route('/url/get/<key>', methods=["GET"])
def get_key(key):
    grabbed_key = redis_client.get(key)
    return jsonify(grabbed_key.decode('utf-8'))

@app.route('/url/delete/<key>', methods=["DELETE"])
def delete_key(key):
    key_to_delete = redis_client.delete(key)
    return jsonify("key has been deleted.")


if __name__ == "__main__":
    app.run(debug=True)
