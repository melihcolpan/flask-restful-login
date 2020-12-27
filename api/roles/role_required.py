#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import logging

from flask import request

import api.error.errors as error
from api.conf.auth import jwt

# from werkzeug.datastructures import Authorization


def permission(arg):
    def check_permissions(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):

            # Get request authorization.
            auth = request.authorization

            # Check if auth is none or not.
            if auth is None and "Authorization" in request.headers:

                try:
                    # Get auth type and token.
                    auth_type, token = request.headers["Authorization"].split(None, 1)
                    # auth = Authorization(auth_type, {'token': token})

                    # Generate new token.
                    data = jwt.loads(token)

                    # Check if admin
                    if data["admin"] < arg:

                        # Return if user is not admin.
                        return error.NOT_ADMIN

                except ValueError:
                    # The Authorization header is either empty or has no token.
                    return error.HEADER_NOT_FOUND

                except Exception as why:
                    # Log the error.
                    logging.error(why)

                    # If it does not generated return false.
                    return error.INVALID_INPUT_422

            # Return method.
            return f(*args, **kwargs)

        # Return decorated method.
        return decorated

    # Return check permissions method.
    return check_permissions
