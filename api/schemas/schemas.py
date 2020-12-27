#!/usr/bin/python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class BaseUserSchema(Schema):

    """
    Base user schema returns all fields but this was not used in user handlers.
    """

    # Schema parameters.

    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    created = fields.Str()


class UserSchema(Schema):

    """
    User schema returns only username, email and creation time. This was used in user handlers.
    """

    # Schema parameters.

    username = fields.Str()
    email = fields.Str()
    created = fields.Str()
