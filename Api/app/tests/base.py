"""Base testcase for all testcase."""
import unittest
import json

# local imports
from app.api import create_app
from app.DB.table_db import create_tables, drop_tables
from app.api import db


class BaseApiTestcase(unittest.TestCase):
    """Setup."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user_details = {
            'username': 'Joetest',
            'email': 'joe@email.com',
            'password': 'U#76pJr3r',
        }

    def tearDown(self):
        """Teardown all initialized variables."""
        drop_tables(db)
        create_tables(db)