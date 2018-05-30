import os
from flask import Flask
from flask_restplus import Api
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])

api = Api(app, version='1.0', title='Maintenance Tracker')

from . import views
