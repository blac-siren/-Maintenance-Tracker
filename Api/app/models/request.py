"""Module for request."""
from app.DB import manage


class CreateRequest:
    """Class for request model."""

    def __init__(self,
                 user_request,
                 category,
                 location,
                 created_by,
                 status='pending'):

        self.user_request = user_request
        self.category = category
        self.location = location
        self.status = status
        self.created_by = created_by

    def save_request(self):
        """Save request in a db."""
        manage.insert_request(self.user_request, self.category, self.location,
                              self.status, self.created_by)
