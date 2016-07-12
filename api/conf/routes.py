#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api
from api.handlers.UserHandlers import Login, RefreshToken, Data


def generate_routes(app):
    api = Api(app)
    api.add_resource(Login, '/v1/auth/login')
    api.add_resource(RefreshToken, '/v1/auth/refresh')
    api.add_resource(Data, '/data')
