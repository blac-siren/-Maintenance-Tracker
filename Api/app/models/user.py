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
        manage.insert_user(self.username, self.email, self.password_hash)

    def __repr__(self):
        """Representation of the class."""
        return "<Username>>>> {}".format(self.username)
