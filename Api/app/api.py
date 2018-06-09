"""Main module."""

from flask import Blueprint
from flask_restplus import Api
from app.routes.auth import auth_namespace as auth
from app.routes.all_requests import request_namespace as request

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    version='1.0',
    authorizations=authorization,
    title='Maintenance Tracker',
    description='Api with endpoints',
    prefix='/api/v1')

api.add_namespace(auth, path='/auth')
api.add_namespace(request, path='/users')
