from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

jwt = JWT('top secret!', expires_in=3600)
refresh_jwt = JWT('telelelele')

auth = HTTPTokenAuth('Bearer')
