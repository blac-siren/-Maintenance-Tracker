"""Module for user."""
from flask_bcrypt import Bcrypt
import datetime
import jwt

# local imports
from app import manage


class User:
    """Store user info into dictionary."""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def save_user(self):
        """Save user in database."""
        manage.insert_user(self.username, self.email, self.password_hash)

    @staticmethod
    def generate_token(user_id):
        """Generate Auth Token."""
        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                user_id
            }
            jwt_token = jwt.encode(payload, 'X3HR4&asrplb', algorithm='HS256')
            return jwt_token
        except Exception as e:
            return e

    def __repr__(self):
        """Representation of the class."""
        return "<Username>>>> {}".format(self.username)
