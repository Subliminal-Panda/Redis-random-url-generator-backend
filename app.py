from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_heroku import Heroku


import random
import string

app = Flask(__name__)
CORS(app)
redis_client = FlaskRedis(app)


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
