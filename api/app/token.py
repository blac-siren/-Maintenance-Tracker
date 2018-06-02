""" Token required for authentication."""
from functools import wraps
from flask import request, jsonify, make_response
import jwt

# local imports
from app import app


def token_required(f):
    """Check if token is present in request header."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Wrap the function."""
        token = None

        # get token from header
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        # Verify token access
        if not token:
            return make_response(
                jsonify({
                    'message':
                    'Unauthorized access. Token access Missing!.'
                }), 401)
        try:
            # decode token and get current_user
            data = jwt.decode(token, app.config.get('SECRET'))
            current_user = data['sub']
        except jwt.ExpiredSignature:
            return make_response(
                jsonify({
                    'Message': 'Token has expired login again'
                }), 401)
        except jwt.InvalidTokenError:
            return make_response(
                jsonify({
                    'Message': 'Invalid token access'
                }), 402)

        if not current_user:
            return make_response(jsonify({'Message': 'Invalid login'}), 401)
        print("dddddddddddddddddddddd", current_user)
        return f(current_user, *args, **kwargs)

    return wrapper