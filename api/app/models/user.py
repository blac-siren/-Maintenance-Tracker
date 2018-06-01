"""Module for storing data in dictionary."""
from flask_bcrypt import Bcrypt
import datetime
import uuid
import jwt

# local imports
from app import app


class User:
    """Store user info into dictionary."""

    user_info = {}

    def __init__(self, username, email, password):
        self.public_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def create_user(self):
        """Save user info into dictionary."""
        user_detail = {
            "email": self.email,
            'username': self.username,
            'id': self.public_id,
            'password': self.password_hash
        }

        User.user_info.update(user_detail)
        return user_detail

    def generate_token(self, user_id):
        """Generate Auth Token."""
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            self, payload, app.config.get('SECRET_KEY'), algorithm='HS256')

    def __repr__(self):
        """Representation of the model."""
        return '<Username> {}'.format(self.username)
