# -*- coding: utf-8 -*-

import copy

# not production-ready solution, just for testing tests
ROOT_NAME = "root"
sessions = set()
accounts = {
    ROOT_NAME: {
        "password": "root"
        # isExternalAccount=true <=> password=None
    }
}
uid_to_login = {
    0: ROOT_NAME
}
new_uid = 1

password_policy = {
    "length": 0,
    "numbers": False,
    "uppercase letters": False,
    "lowercase letters": False,
    "special symbols": False
}

NUMBERS = set("0123456789")
LETTERS = "qwertyuiopasdfghjklzxcvbnm"
UPPERCASE_LETTERS = set(LETTERS.upper())
LOWERCASE_LETTERS = set(LETTERS.lower())
SPECIAL_SYMBOLS = set("!@#$%^&*()_-+=")


def get_password_problem(password, password_policy):
    if len(password) < password_policy["length"]:
        return "Password MUST contain at least {} symbols".format(password_policy["length"])

    password_symbols = set(password)

    if password_policy["numbers"] and not (password_symbols & NUMBERS):
        return "Password MUST contain at least 1 number"

    if password_policy["uppercase letters"] and not (password_symbols & UPPERCASE_LETTERS):
        return "Password MUST contain at least 1 uppercase letter"

    if password_policy["lowercase letters"] and not (password_symbols & LOWERCASE_LETTERS):
        return "Password MUST contain at least 1 lowercase letter"

    if password_policy["special symbols"] and not (password_symbols & SPECIAL_SYMBOLS):
        return "Password MUST contain at least 1 special symbol"

    return None


def get_accounts():
    return 200, [(key, value) for key,value in uid_to_login.items()]


def new_account(body):
    if body["login"] in accounts:
        return 400, {
            "info": "Account with this login already exists"
        }
    if not body["isExternalAccount"]:
        password_problem = get_password_problem(body["password"], password_policy)
        if password_problem:
            return 400, {
                "info": password_problem
            }
    else:
        assert body["password"] is None
    accounts[body["login"]] = {
        "password": body["password"]
    }
    global new_uid
    uid_to_login[new_uid] = body["login"]
    new_uid += 1
    return 201, {
        "id": new_uid - 1
    }


def change_password(uid, body):
    body["login"] = uid_to_login[uid]
    if body["login"] not in accounts:
        return 400, {
            "info": "Login not exists"
        }
    if accounts[body["login"]]["password"] is None:
        return 400, {
            "info": "External account"
        }
    if accounts[body["login"]]["password"] != body["oldPassword"]:
        return 400, {
            "info": "Invalid password"
        }
    password_problem = get_password_problem(body["newPassword"], password_policy)
    if password_problem:
        return 400, {
            "info": password_problem
        }
    accounts[body["login"]]["password"] = body["newPassword"]
    return 201, {}


def delete_account(uid):
    if uid == 0:
        return 400, {
            "info": "Unable to delete root"
        }
    if uid not in uid_to_login:
        return 400, {
            "info": "Account not exists"
        }
    user_login = uid_to_login[uid]
    logout({
        "login": user_login
    })
    del uid_to_login[uid]
    del accounts[user_login]
    return 200, {}


def login(body):
    if body["login"] not in accounts:
        return 400, {
            "info": "Login not exists"
        }
    if accounts[body["login"]]["password"] is None:
        # external account
        sessions.add(body["login"])
        return 201, {}
    if body["password"] != accounts[body["login"]]["password"]:
        return 403, {
            "info": "Invalid password"
        }

    sessions.add(body["login"])
    return 201, {}


def logout(body):
    if body["login"] not in sessions:
        return 400, {
            "info": "User not logged in"
        }
    sessions.remove(body["login"])
    return 201, {}


def set_policy(body):
    global password_policy
    if set(body.keys()) != {
            "length",
            "numbers",
            "uppercase letters",
            "lowercase letters",
            "special symbols"
    }:
        # some checks may be here
        pass
    password_policy = copy.copy(body)
    return 201, {}
