"""Module for request."""


class CreateRequest:
    """Class saves request."""

    all_requests = []

    def __init__(self, user_request, category, location):

        self.user_request = user_request
        self.category = category
        self.location = location

    def save_request(self):
        """Save request in a dictionary."""
        requests = {
            'id': len(CreateRequest.all_requests) + 1,
            'user_request': self.user_request,
            'category': self.category,
            'location': self.location
        }

        CreateRequest.all_requests.append(requests)
        return requests
