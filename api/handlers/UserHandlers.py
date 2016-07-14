#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import api.error.errors as error
from flask_restful import Resource
from flask import request
from api.conf.auth import refresh_jwt
from api.models.models import User, Blacklist
from api.conf.auth import auth
from api.database.database import db
from flask import g


class Register(Resource):
    @staticmethod
    def post():

        # Get username, password and email.
        username, password, email = request.json.get('username').strip(), request.json.get('password').strip(), \
                                    request.json.get('email').strip()

        # Check if any field is none.
        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = User(username=username, password=password, email=email)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        User.query.filter_by(email=email, password=password).first()

        # Return success if registration is completed.
        return {'status': 'registration completed.'}


class Login(Resource):
    @staticmethod
    def post():

        # Get user email and password.
        email, password = request.json.get('email').strip(), request.json.get('password').strip()

        # Check if user information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email, password=password).first()

        # Check if user is not existed.
        if user is None:
            return error.DOES_NOT_EXIST

        # Generate access token.
        access_token = user.generate_auth_token()

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({'email': email})

        # Return access token and refresh token.
        return {'access_token': access_token, 'refresh_token': refresh_token}


class Logout(Resource):
    @staticmethod
    def post():

        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        # Create a blacklist refresh token.
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        if blacklist_refresh_token is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}

        # Add refresh token to session.
        db.session.add(blacklist_refresh_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {'status': 'invalidated', 'refresh_token': refresh_token}


class RefreshToken(Resource):
    @staticmethod
    def post():

        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        # Get if the refresh token is in blacklist.
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        # Check refresh token is existed.
        if ref is not None:

            # Return invalidated token.
            return {'status': 'invalidated'}

        try:
            # Generate new token.
            data = refresh_jwt.loads(refresh_token)

        except Exception as why:
            # Log the error.
            logging.error(why)

            # If it does not generated return false.
            return False

        # Create user not to add db. For generating token.
        user = User(email=data['email'])

        # New token generate.
        token = user.generate_auth_token()

        # Return new access token.
        return {'access_token': token}


class ResetPassword(Resource):
    @auth.login_required
    def post(self):

        # Get old and new passwords.
        old_pass, new_pass = request.json.get('old_pass'), request.json.get('new_pass')

        # Get user. g.user generates email address cause we put email address to g.user in models.py.
        user = User.query.filter_by(email=g.user).first()

        # Check if user password does not match with old password.
        if user.password != old_pass:

            # Return does not match status.
            return {'status': 'old password does not match.'}

        # Update password.
        user.password = new_pass

        # Commit session.
        db.session.commit()

        # Return success status.
        return {'status': 'password changed.'}


class Data(Resource):
    @auth.login_required
    def get(self):

        # Return some data from db.
        return "Test data got!"
