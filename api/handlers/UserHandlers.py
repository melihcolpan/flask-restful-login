#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request, make_response, jsonify
from api.conf.auth import refresh_jwt
from api.models.models import User
from api.conf.auth import auth
from api.database.database import db
import api.error.errors as error


class Login(Resource):
    @staticmethod
    def post():

        # Get user email and password.
        email, password = request.json.get('email').strip(), request.json.get('password').strip()

        # Check if user information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create new user.
        user = User(email=email)

        # Add user to database session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Generate access token.
        access_token = user.generate_auth_token()

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({'email': email})

        # Return access token and refresh token.
        return make_response(jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200)


class RefreshToken(Resource):
    @staticmethod
    def post():
        refresh_token = request.json.get('refresh_token')
        try:
            data = refresh_jwt.loads(refresh_token)
        except:
            return False

        user = User(email=data['email'])
        token = user.generate_auth_token()

        return {'access_token': token}


class Data(Resource):
    @auth.login_required
    def get(self):
        return "data OK"
