#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.db_initializer.db_initializer import create_test_user
from api.database.database import db
from api.tests.base import BaseTest

USERS_QUERY = "/users?usernames=normal&emails=normal@test.com&start_date=01.01.2000&end_date=01.01.2100"


class RoleTest(BaseTest):
    def token_for(self, role):
        user = create_test_user(username=role, password="secret", email=f"{role}@test.com")
        user.user_role = role
        db.session.commit()
        response = self.client.post("/v1/auth/login", json={"email": f"{role}@test.com", "password": "secret"})
        assert response.status_code == 200
        return response.json["access_token"]

    def get(self, path, token=None, header=None):
        headers = {"Authorization": header if header is not None else f"Bearer {token}"}
        return self.client.get(path, headers=headers)

    def test_normal_user_is_denied_admin_routes(self):
        token = self.token_for("user")
        for path in ("/data_admin", "/data_super_admin", USERS_QUERY):
            response = self.get(path, token)
            assert response.status_code == 403, (path, response.status_code, response.json)

    def test_normal_user_can_use_user_route(self):
        assert self.get("/data_user", self.token_for("user")).status_code == 200

    def test_admin_is_allowed_admin_but_not_super_admin_routes(self):
        token = self.token_for("admin")
        assert self.get("/data_admin", token).status_code == 200
        assert self.get("/data_super_admin", token).status_code == 403
        assert self.get(USERS_QUERY, token).status_code == 403

    def test_super_admin_is_allowed_everything(self):
        token = self.token_for("sa")
        assert self.get("/data_admin", token).status_code == 200
        assert self.get("/data_super_admin", token).status_code == 200
        assert self.get(USERS_QUERY, token).status_code == 200

    def test_missing_or_invalid_tokens_are_rejected(self):
        self.token_for("user")
        for header in ("", "Bearer", "Bearer not-a-token", "Basic dXNlcjpwYXNz"):
            for path in ("/data_admin", "/data_super_admin"):
                assert self.get(path, header=header).status_code == 401, (path, header)
        assert self.client.get("/data_admin").status_code == 401
