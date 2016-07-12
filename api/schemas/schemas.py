#!/usr/bin/python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str()
