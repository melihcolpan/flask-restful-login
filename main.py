#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from api.database.database import db
from api.conf.config import SQLALCHEMY_DATABASE_URI
from api.conf.routes import generate_routes
from api.db_initializer.db_initializer import create_admin_user, create_test_user


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)

    if not os.path.exists(SQLALCHEMY_DATABASE_URI):
        db.app = app
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    db.create_all()
    create_admin_user()
    create_test_user()
    generate_routes(app)
    app.run()
