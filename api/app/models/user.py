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

    def __repr__(self):
        """Representation of the class."""
        return "<Username>>>> {}".format(self.username)
