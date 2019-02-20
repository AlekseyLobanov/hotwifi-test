# -*- coding: UTF-8

from importlib import reload
import unittest

from core.handlers import login, logout, new_account, set_policy
from core.handlers import change_password, get_accounts, delete_account

class TestBase(unittest.TestCase):
    def setUp(self):
        import core.handlers
        reload(core.handlers)

    def test_root_login(self):
        self.assertEqual(
            login({
                "login": "root",
                "password": "not root"
            })[0],
            403
        )
        self.assertEqual(
            login({
                "login": "root",
                "password": "root"
            })[0],
            201
        )
        self.assertEqual(
            logout({
                "login": "root"
            })[0],
            201
        )
        self.assertEqual(
            logout({
                "login": "root"
            })[0],
            400
        )

    def test_password_policy(self):
        self.assertEqual(
            new_account({
                "login": "alice",
                "password": "test",
                "isExternalAccount": False
            })[0],
            201
        )
        self.assertEqual(
            set_policy({
                "length": 8,
                "numbers": True,
                "uppercase letters": True,
                "lowercase letters": True,
                "special symbols": True
            })[0],
            201
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "abcd"
            })[0],
            400
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "abcdabcdabcd"
            })[0],
            400
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "abcdabcdabcd12"
            })[0],
            400
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "ABCDABCDABCD12"
            })[0],
            400
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "abcdabcdabcd12QWE"
            })[0],
            400
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "test",
                "newPassword": "abcdabcdabcd12QWE!"
            })[0],
            201
        )
        self.assertEqual(
            set_policy({
                "length": 4,
                "numbers": False,
                "uppercase letters": False,
                "lowercase letters": False,
                "special symbols": False
            })[0],
            201
        )
        self.assertEqual(
            change_password(1, {
                "oldPassword": "abcdabcdabcd12QWE!",
                "newPassword": "abcd"
            })[0],
            201
        )

    def test_account_creation(self):
        set_policy({
            "length": 8,
            "numbers": False,
            "uppercase letters": False,
            "lowercase letters": False,
            "special symbols": False
        })
        self.assertEqual(
            new_account({
                "login": "root",
                "password": "sadasdsadfafdsf",
                "isExternalAccount": False
            })[0],
            400
        )
        self.assertEqual(
            new_account({
                "login": "alice",
                "password": "test",
                "isExternalAccount": False
            })[0],
            400
        )
        self.assertTupleEqual(
            new_account({
                "login": "alice",
                "password": "dasdsadsadfsa",
                "isExternalAccount": False
            }),
            (201, {"id": 1})
        )

    def test_account_delete(self):
        self.assertEqual(
            delete_account(0)[0],
            400
        )
        new_account({
            "login": "alice",
            "password": "dasdsadsadfsa",
            "isExternalAccount": False
        })
        self.assertEqual(
            delete_account(1)[0],
            200
        )
        self.assertEqual(
            delete_account(1)[0],
            400
        )

    def test_get_accounts(self):
        self.assertTupleEqual(
            get_accounts(),
            (
                200,
                [(0, "root")]
            )
        )
        new_account({
            "login": "alice",
            "password": "31",
            "isExternalAccount": False
        })
        new_account({
            "login": "bob",
            "password": None,
            "isExternalAccount": True
        })
        self.assertTupleEqual(
            get_accounts(),
            (
                200,
                [(0, "root"), (1, "alice"), (2, "bob")]
            )
        )
        delete_account(1)
        self.assertTupleEqual(
            get_accounts(),
            (
                200,
                [(0, "root"), (2, "bob")]
            )
        )
