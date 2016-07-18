#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.database.database import db
from api.models.models import User


def create_admin_user():

    # Check if admin is existed in db.
    user = User.query.filter_by(email='admin').first()

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        user = User(username='admin_username', password='admin_password', email='admin_email@example.com', user_role='admin')

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Print admin user status.
        print("Admin was set.")

    else:
        # Print admin user status.
        print("Admin already set.")


def create_test_user():

    # Check if admin is existed in db.
    user = User.query.filter_by(email='test_username').first()

    # If user is none.
    if user is None:

        # Create admin user if it does not existed.
        user = User(username='test_username', password='test_password', email='test_email@example.com',
                    user_role='user')

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Print admin user status.
        print("Test user was set.")

    else:

        # Print admin user status.
        print("User already set.")
