#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.database.database import db
from api.db_initializer.db_initializer import create_test_user
from api.tests.base import BaseTest


class PasswordTest(BaseTest):
    def register(self, password, email="pw@test.com"):
        return self.client.post(
            "/v1/auth/register", json={"username": "pw", "password": password, "email": email}
        )

    def login(self, password, email="pw@test.com"):
        return self.client.post("/v1/auth/login", json={"email": email, "password": password})

    def test_password_is_used_exactly_as_typed(self):
        assert self.register("  spaced pass  ").status_code == 200
        assert self.login("  spaced pass  ").status_code == 200
        assert self.login("spaced pass").status_code == 401

    def test_whitespace_only_password_is_rejected(self):
        assert self.register(" " * 10).status_code == 422

    def test_password_longer_than_72_bytes_is_rejected_not_a_server_error(self):
        assert self.register("p" * 73).status_code == 422
        assert self.register("ş" * 37).status_code == 422  # 74 bytes in UTF-8
        assert self.register("p" * 72).status_code == 200

    def test_long_password_on_login_is_a_wrong_credential(self):
        assert self.register("p" * 72).status_code == 200
        assert self.login("p" * 200).status_code == 401

    def test_non_string_password_is_rejected(self):
        assert self.register(12345678).status_code == 422
        assert self.register("secret-pass").status_code == 200
        assert self.login(None).status_code == 422  # missing field
        assert self.login(12345678).status_code == 401

    def test_account_created_with_a_stripped_password_can_still_log_in(self):
        # Before this change, " secret-pass " was stored as "secret-pass".
        create_test_user(username="old", password="secret-pass", email="old@test.com")
        assert self.login(" secret-pass ", email="old@test.com").status_code == 200
        assert self.login("secret-pass", email="old@test.com").status_code == 200

    def test_password_reset_uses_the_same_policy(self):
        assert self.register("secret-pass").status_code == 200
        token = self.login("secret-pass").json["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        def reset(old, new):
            return self.client.post(
                "/v1/auth/password_reset", json={"old_pass": old, "new_pass": new}, headers=headers
            )

        assert reset("secret-pass", "p" * 100).status_code == 422
        assert reset("secret-pass", " " * 9).status_code == 422
        assert reset(None, "new-secret-pass").json == {"status": "old password does not match."}
        assert reset("secret-pass", " new secret ").json == {"status": "password changed."}
        db.session.expire_all()
        assert self.login(" new secret ").status_code == 200
