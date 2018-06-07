"""Run the application."""
import os
from flask import Flask
from app import api
from app.configuration.config import app_config

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])

if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)