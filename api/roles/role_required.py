#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import logging

from flask import request

import api.error.errors as error
from api.conf.auth import jwt


def permission(arg):
    """Allow the request only if its Bearer token grants at least role ``arg``.

    Roles: user=0, admin=1, super admin=2. Any request without a valid Bearer
    token, or whose token does not grant the role, is rejected (deny by default).
    """

    def check_permissions(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):

            # Werkzeug parses the Authorization header, including Bearer tokens.
            auth = request.authorization
            if auth is None or auth.type != "bearer" or not auth.token:
                return error.UNAUTHORIZED

            try:
                data = jwt.loads(auth.token)
            except Exception as why:
                logging.info("Rejected token in permission check: %s", why)
                return error.UNAUTHORIZED

            # Deny unless the token explicitly grants a high enough role.
            role = data.get("admin") if isinstance(data, dict) else None
            if not isinstance(role, int) or role < arg:
                return error.NOT_ADMIN

            return f(*args, **kwargs)

        return decorated

    return check_permissions
