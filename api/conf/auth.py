#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

# JWT creation.
jwt = JWT('top secret!', expires_in=3600)

# Refresh token creation.
refresh_jwt = JWT('telelelele', expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth('Bearer')
