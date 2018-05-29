"""Module for storing data in dictionary."""
from flask_bcrypt import Bcrypt
import datetime
import jwt
import uuid


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
        user_details = {
            self.email: {
                'username': self.username,
                'id': self.public_id,
                'password': self.password_hash
            }
        }
        User.user_info.update(user_details)
        return user_details

    def __repr__(self):
        return '<Username> {}'.format(self.username)
