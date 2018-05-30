"""Module for request."""


class CreateRequest:
    """Class saves request."""

    all_requests = []
    id = 1

    def __init__(self, request, category, location):

        self.request = request
        self.category = category
        self.location = location

    def save_request(self):
        """Save request in a dictionary."""
        requests = {
            CreateRequest.id: {
                'request': self.request,
                'category': self.category,
                'location': self.location
            }
        }
        CreateRequest.all_requests.append(requests)
        CreateRequest.id += 1
        return requests
