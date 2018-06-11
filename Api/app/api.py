from flask import Flask
from flask_restplus import Api
from app.configuration.config import app_config
from app.DB.table_db import TrackerDB

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'access_token'
    }
}

api = Api(
    version='1.0',
    authorizations=authorization,
    title='Maintenance Tracker',
    description='Api with endpoints',
    prefix='/api/v1')

# delete default namespace.
del api.namespaces[0]

db = TrackerDB()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(config_name)

    from app.routes.admin import ns as admin
    from app.routes.auth import auth_namespace as auth
    from app.routes.all_requests import request_namespace as request

    api.add_namespace(auth, path='/auth')
    api.add_namespace(request, path='/users')
    api.add_namespace(admin, path='/requests')
    api.init_app(app)
    return app
