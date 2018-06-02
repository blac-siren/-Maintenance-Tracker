"""Module for storing data in dictionary."""
from flask_bcrypt import Bcrypt
import datetime
import uuid
import jwt

# local imports
from app import app


class User:
    """Store user info into dictionary."""

    user_info = []

    def __init__(self, username, email, password):
        self.public_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def create_user(self):
        """Save user info into dictionary."""
        user_detail = {
            'id': len(User.user_info) + 1,
            "email": self.email,
            'username': self.username,
            'user_id': self.public_id,
            'password': self.password_hash
        }

        User.user_info.append(user_detail)
        return user_detail

    @staticmethod
    def generate_token(user_id):
        """Generates Auth Token."""
        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            jwt_token = jwt.encode(
                payload, app.config.get('SECRET'), algorithm='HS256')
            return jwt_token
        except Exception as e:
            return str(e)

    def __repr__(self):
        """Representation of the class."""
        return "<Username>>>> {}".format(self.username)
