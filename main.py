#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask

from core.handlers import *

app = Flask(__name__)

@app.route("/api/accounts", methods=['GET'])
def base_get_accounts():
    return json.dumps(get_accounts())

@app.route("/api/accounts", methods=['POST'])
def base_new_account():
    return json.dumps(new_account())

@app.route("/api/accounts/<uid>/password", methods=['PUT'])
def base_change_password():
    return json.dumps(change_password(uid))

@app.route("/api/accounts/<uid>", methods=['DELETE'])
def base_delete_account():
    return json.dumps(delete_account(uid))

@app.route("/api/accounts/login", methods=['POST'])
def base_login():
    return json.dumps(login())

@app.route("/api/accounts/logout", methods=['POST'])
def base_logout():
    return json.dumps(logout())

@app.route("/api/accounts/password/policy", methods=['POST'])
def base_set_policy():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
