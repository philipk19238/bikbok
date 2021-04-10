import os 

from flask import Flask

def register_blueprints(app):
    pass

def create_app():
    app = Flask(__name__)
    
    register_blueprints(app)