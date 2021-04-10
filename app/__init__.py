import os 

from flask import Flask
from .config import config

def register_blueprints(app):
    pass

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)

    return app