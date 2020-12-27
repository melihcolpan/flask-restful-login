#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_testing import TestCase

from api.database.database import db
from main import create_app


class BaseTest(TestCase):

    # Set test database as sqlite memory database or use test database.
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):

        # pass in test configuration
        return create_app()

    # Set up database tables.
    def setUp(self):

        db.create_all()

    # Remove all database and tables.
    def tearDown(self):

        db.session.remove()
        db.drop_all()
