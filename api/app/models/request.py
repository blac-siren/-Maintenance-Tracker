"""Module for request."""


class CreateRequest:
    """Class saves request."""

    all_requests = {}
    id = 1

    def __init__(self, req, category, location):

        self.req = req
        self.category = category
        self.location = location

    def save_request(self):
        """Save request in a dictionary."""
        requests = {
            CreateRequest.id: {
                'req': self.req,
                'category': self.category,
                'location': self.location
            }
        }

        CreateRequest.all_requests.update(requests)
        CreateRequest.id += 1
        return requests
