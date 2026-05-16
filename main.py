#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask

from api.conf.config import SQLALCHEMY_DATABASE_URI
from api.conf.routes import generate_routes
from api.database.database import db


def create_app():

    # Create a flask app.
    app = Flask(__name__)

    # Set secret key from environment.
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable must be set. "
            "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
        )
    app.config["SECRET_KEY"] = SECRET_KEY

    # Set debug from environment (default: False for production safety).
    app.config['DEBUG'] = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

    # Set database url.
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Generate routes.
    generate_routes(app)

    # Database initialize with app.
    db.init_app(app)

    # Check if there is no database.
    if not os.path.exists(SQLALCHEMY_DATABASE_URI):

        # New db app if no database.
        db.app = app

        # Create all database tables.
        db.create_all()

    # Return app.
    return app


if __name__ == '__main__':

    # Create app.
    app = create_app()

    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)
