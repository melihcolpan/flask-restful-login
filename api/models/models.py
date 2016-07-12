import logging

from api.database.database import db
from api.conf.auth import jwt, auth
from flask import g


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=80))
    password = db.Column(db.String(length=80))

    def generate_auth_token(self):
        token = jwt.dumps({'email': self.email})
        return token

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
