#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api
from api.handlers.UserHandlers import Register, Login, Logout, RefreshToken, UsersData, ResetPassword


def generate_routes(app):
    api = Api(app)
    api.add_resource(Register, '/v1/auth/register')
    api.add_resource(Login, '/v1/auth/login')
    api.add_resource(Logout, '/v1/auth/logout')
    api.add_resource(RefreshToken, '/v1/auth/refresh')
    api.add_resource(ResetPassword, '/v1/auth/password_reset')

    api.add_resource(UsersData, '/users')
