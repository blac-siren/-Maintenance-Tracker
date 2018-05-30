"""Module for storing data in dictionary."""
from flask_bcrypt import Bcrypt
import datetime
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
        user_detail = {
            self.email: {
                'username': self.username,
                'id': self.public_id,
                'password': self.password_hash
            }
        }

        User.user_info.update(user_detail)
        return user_detail

    def password_is_valid(self, password):
        """Validate password against its hash"""
        return Bcrypt().check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Username> {}'.format(self.username)
