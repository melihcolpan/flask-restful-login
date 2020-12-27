#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Create a database in project and get it's path.
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")
