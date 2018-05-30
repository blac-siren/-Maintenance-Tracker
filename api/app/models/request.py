"""Module for request."""


class Request:
    """Class saves request."""

    requests = []

    def __init__(self, request, category, location):
        self.request = request
        self.category = category
        self.location = location

    def save_request(self):
        """Save request in a dictionary."""
        request = {
            'request': self.request,
            'category': self.category,
            'location': self.location
        }
        Request.requests.append(request)
        return request
