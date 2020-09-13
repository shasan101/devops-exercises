#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask import make_response

import json
from werkzeug.exceptions import NotFound


app = Flask(__name__)

with open("./users.json", "r") as f:
    users = json.load(f)


@app.route("/", methods=['GET'])
def index():
    return pretty_json({
        "resources": {
            "users": "/users",
            "user": "/users/<username>",
        },
        "current_uri": "/"
    })


@app.route("/users", methods=['GET'])
def all_users():
#    print(type(users))
    users_without_id = {}
    for user in users:
        users_without_id[user] = {}
        for attribute in users[user]:
            if attribute not in "id":
                users_without_id[user][attribute] = users[user][attribute]
                #print(users_without_id[user])
                #print(users_without_id[user][attribute])
    #print(users_without_id)
    return pretty_json(users_without_id)


@app.route("/users/<username>", methods=['GET'])
def user_data(username):
    if username not in users:
        raise NotFound

    return pretty_json(users[username])


@app.route("/users/<username>/something", methods=['GET'])
def user_something(username):
    raise NotImplementedError()


def pretty_json(arg):
    #print("arg: ", arg)
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


def create_test_app():
    app = Flask(__name__)
    return app


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
