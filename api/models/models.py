#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.database.database import db
from api.conf.auth import jwt, auth
from flask import g
from datetime import datetime


class User(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Table fields.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=80))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_role = db.Column(db.String, default='user')

    # Generates auth token.
    def generate_auth_token(self, admin_check):

        # Check if admin.
        if admin_check:

            # Generate admin token with flag 1.
            token = jwt.dumps({'email': self.email, 'admin': 1})

            # Return admin flag.
            return token

        # Return normal user flag.
        return jwt.dumps({'email': self.email, 'admin': 0})

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except:
            return False
        if 'email' and 'admin' in data:
            g.user = data['email']
            g.admin = data['admin']
            return True
        return False

    def __repr__(self):
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
                      self.id, self.username, self.password, self.email, self.created)


class Blacklist(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Blacklist fields.
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
                      self.id, self.refresh_token)
