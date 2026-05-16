#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# Get JWT secret from environment.
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable must be set")

# Get refresh JWT secret from environment.
REFRESH_JWT_SECRET = os.environ.get("REFRESH_JWT_SECRET")
if not REFRESH_JWT_SECRET:
    raise RuntimeError("REFRESH_JWT_SECRET environment variable must be set")

# JWT creation.
jwt = JsonWebToken(JWT_SECRET, expires_in=3600)

# Refresh token creation.
refresh_jwt = JsonWebToken(REFRESH_JWT_SECRET, expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
