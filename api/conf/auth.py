#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# JWT creation.
jwt = JsonWebToken("top secret!", expires_in=3600)

# Refresh token creation.
refresh_jwt = JsonWebToken("telelelele", expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
