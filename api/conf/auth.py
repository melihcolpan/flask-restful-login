#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask_httpauth import HTTPTokenAuth
from itsdangerous import URLSafeTimedSerializer

# Read JWT secret from environment.
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable must be set.")

# Read refresh JWT secret from environment.
REFRESH_JWT_SECRET = os.environ.get("REFRESH_JWT_SECRET")
if not REFRESH_JWT_SECRET:
    raise RuntimeError("REFRESH_JWT_SECRET environment variable must be set.")


class TimedToken:
    """Signed, expiring token serializer.

    Wraps itsdangerous' URLSafeTimedSerializer to keep the dumps()/loads()
    interface the rest of the code relies on. ``loads`` rejects tokens older
    than ``expires_in`` seconds by raising ``itsdangerous.SignatureExpired``.
    """

    def __init__(self, secret, expires_in):
        self.serializer = URLSafeTimedSerializer(secret)
        self.expires_in = expires_in

    def dumps(self, data):
        # Return bytes so existing .decode() call sites keep working.
        return self.serializer.dumps(data).encode("utf-8")

    def loads(self, token):
        return self.serializer.loads(token, max_age=self.expires_in)


# JWT creation.
jwt = TimedToken(JWT_SECRET, expires_in=3600)

# Refresh token creation.
refresh_jwt = TimedToken(REFRESH_JWT_SECRET, expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
