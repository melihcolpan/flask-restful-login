#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

jwt = JWT('top secret!', expires_in=60)
refresh_jwt = JWT('telelelele', expires_in=120)

auth = HTTPTokenAuth('Bearer')
