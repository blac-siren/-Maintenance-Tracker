"""Common function for the app."""
from functools import wraps
from flask import request, make_response, jsonify
import jwt


def token_required(f):
    """Decorate to check if valid token present in request header."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Wrap function."""
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        # Verifies token is present
        if not token:
            return {'Message': "Unauthorized, access token required!"}, 401
        try:
            # try to decode using token and secret key
            payload = jwt.decode(token, 'X3HR4&asrplb')
            user_id = payload['sub']
        except jwt.ExpiredSignature:
            return {'Message': 'Expired token. Please log in.'}
        except jwt.InvalidTokenError:
            return {'Message': 'Invalid token. Please register or log in'}

        return f(user_id, *args, **kwargs)

    return wrapper