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

    # Generates auth token.
    def generate_auth_token(self):
        token = jwt.dumps({'email': self.email})
        return token

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except:
            return False
        if 'email' in data:
            g.user = data['email']
            return True
        return False

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (
                      self.email, self.password)


class Blacklist(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Blacklist fields.
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):
        return "<User(refresh_token='%s', status='invalidated.')>" % (
                      self.refresh_token)
