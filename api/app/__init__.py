import os
from flask import Flask, Blueprint
from flask_restplus import Api
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    app,
    version='1.0',
    title='Maintenance Tracker',
    description="Maintenance Tracker with REST endpoints",
    authorizations=authorizations,
    prefix='/api/v1')

from . import views
