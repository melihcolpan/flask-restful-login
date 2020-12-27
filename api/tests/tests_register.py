#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.db_initializer.db_initializer import create_test_user
from api.tests.base import BaseTest


class RegisterTest(BaseTest):
    def test_register(self):

        # Expected result from server.
        expected_result = {"status": "registration completed."}

        # User data to register.
        data = {"username": "test", "password": "secret", "email": "test@test.com"}

        # Send request to index.
        response = self.client.post("/v1/auth/register", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 200 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_register_missing_parameter(self):

        # Expected result from server.
        expected_result = {"message": "Invalid input."}

        # User data to register. <username> MISSING parameter.
        data = {"password": "secret", "email": "test@test.com"}

        # Send request to index.
        response = self.client.post("/v1/auth/register", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 422 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json

    def test_register_already_exists(self):

        # Expected result from server.
        expected_result = {"message": "Already exists."}

        # User already created.
        create_test_user(username="test", password="secret", email="test@test.com")

        # User same data to register.
        data = {"username": "test", "password": "secret", "email": "test@test.com"}

        # Send request to index.
        response = self.client.post("/v1/auth/register", json=data)

        # Log if needed.
        # print(f"Status Code: {response.status_code}\nResult: {response.json}")

        # This raises an AssertionError
        assert 409 == response.status_code

        # This raises an AssertionError
        assert expected_result == response.json
