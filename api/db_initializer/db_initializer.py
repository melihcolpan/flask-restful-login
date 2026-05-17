#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from api.database.database import db
from api.models.models import User


def create_super_admin():

    # Check if admin is existed in db.
    user = User.query.filter_by(email="test_username").first()

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        user = User(
            username="sa_username",
            email="sa_email@example.com",
            user_role="sa",
        )
        user.set_password("sa_password")

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Print admin user status.
        logging.info("Super admin was set.")

    else:

        # Print admin user status.
        logging.info("Super admin already set.")


def create_admin_user():

    # Check if admin is existed in db.
    user = User.query.filter_by(email="admin").first()

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        user = User(
            username="admin_username",
            email="admin_email@example.com",
            user_role="admin",
        )
        user.set_password("admin_password")

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Print admin user status.
        logging.info("Admin was set.")

    else:
        # Print admin user status.
        logging.info("Admin already set.")


def create_test_user(
    username="test_username",
    password="test_password",
    email="test_email@example.com",
    user_role="user",
):

    # Check if admin is existed in db.
    user = User.query.filter_by(email="test_username").first()

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        user = User(
            username=username,
            email=email,
            user_role=user_role,
        )
        user.set_password(password)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Print admin user status.
        logging.info("Test user was set.")

        # Return user.
        return user

    else:

        # Print admin user status.
        logging.info("User already set.")
