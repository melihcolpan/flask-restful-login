#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.conf.auth import jwt
from api.db_initializer.db_initializer import create_test_user
from api.tests.base import BaseTest


class LoginTest(BaseTest):
    def test_login(self):

        # User created to login.
        user = create_test_user(
            username="test", password="secret", email="test@test.com"
        )

        # User data to register.
        data = {"email": "test@test.com", "password": "secret"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert response.status_code == 200

        # Check access and refresh token in response.
        assert "access_token" in response.json
        assert "refresh_token" in response.json

        # Get access and refresh tokens.
        access_token = response.json.get("access_token")

        # Load access token and see the data.
        tokenized_data = jwt.loads(access_token)

        # This raises an AssertionError
        assert tokenized_data.get("email") == user.email

        # This raises an AssertionError
        assert tokenized_data.get("admin") == 0

    def test_login_missing_parameter(self):

        # Expected result from server.
        expected_result = {"message": "Invalid input."}

        # User created to login.
        create_test_user(username="test", password="secret", email="test@test.com")

        # User data to register. Password MISSING parameter.
        data = {"email": "test@test.com"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 422 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_login_none_parameter(self):

        # Expected result from server.
        expected_result = {"message": "Invalid input."}

        # User created to login.
        create_test_user(username="test", password="secret", email="test@test.com")

        # User data to register. Password NONE parameter.
        data = {"email": "test@test.com", "password": None}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 422 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_login_doesnt_exist(self):

        # Expected result from server.
        expected_result = {"message": "Does not exists."}

        # User data to register.
        data = {"email": "not-exist-user@test.com", "password": "any-password"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 409 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_login_wrong_password(self):

        # Expected result from server.
        expected_result = {"message": "Wrong credentials."}

        # User created to login.
        create_test_user(username="test", password="secret", email="test@test.com")

        # User data to register.
        data = {"email": "test@test.com", "password": "wrong-password"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 401 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_login_admin(self):

        # User created to login.
        user = create_test_user(
            username="test",
            password="secret",
            email="test-admin@test.com",
            user_role="admin",
        )

        # User data to register.
        data = {"email": "test-admin@test.com", "password": "secret"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert response.status_code == 200

        # Check access and refresh token in response.
        assert "access_token" in response.json
        assert "refresh_token" in response.json

        # Get access and refresh tokens.
        access_token = response.json.get("access_token")

        # Load access token and see the data.
        tokenized_data = jwt.loads(access_token)

        # This raises an AssertionError
        assert tokenized_data.get("email") == user.email

        # This raises an AssertionError
        assert tokenized_data.get("admin") == 1

    def test_login_super_admin(self):

        # User created to login.
        user = create_test_user(
            username="test",
            password="secret",
            email="test-admin@test.com",
            user_role="sa",
        )

        # User data to register.
        data = {"email": "test-admin@test.com", "password": "secret"}

        # Send request to index.
        response = self.client.post("/v1/auth/login", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert response.status_code == 200

        # Check access and refresh token in response.
        assert "access_token" in response.json
        assert "refresh_token" in response.json

        # Get access and refresh tokens.
        access_token = response.json.get("access_token")

        # Load access token and see the data.
        tokenized_data = jwt.loads(access_token)

        # This raises an AssertionError
        assert tokenized_data.get("email") == user.email

        # This raises an AssertionError
        assert tokenized_data.get("admin") == 2
