from .. import mongo, login_manager
from flask import current_app, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User():
    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticate(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def password(password):
        return generate_password_hash(password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'email': self.email}).decode('ascii')

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
