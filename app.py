from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_heroku import Heroku

import psycopg2
import random
import string
import os
import redis

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["REDIS_URL"] = "redis://:pa41016516313b339841974e534113c236901d14f89502d066b45ceadb159897f@ec2-34-237-62-177.compute-1.amazonaws.com:18899"
CORS(app)
redis_client = FlaskRedis(app)
url = urlparse(os.environ.get("REDIS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)


@app.route('/url/add', methods=["POST"])
def add_url():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON.')

    url = request.json.get('url')
    custom_link = request.json.get('custom link')
    if custom_link == None:
        key = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])
    else:
        key = custom_link

    redis_client.set(key, url)
    return jsonify(key)

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
