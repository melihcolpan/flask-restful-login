#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.tests.base import BaseTest


class IndexTest(BaseTest):
    def test_index(self):

        # Expected result from server.
        expected_result = "Hello Flask Restful Example!"

        # Send request to index.
        response = self.client.get("/")

        # This raises an AssertionError
        assert response.status_code == 200

        # This raises an AssertionError
        assert expected_result == response.json
