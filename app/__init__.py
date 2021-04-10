import os 
from werkzeug.debug import DebuggedApplication
from flask import Flask
from .config import config

def register_blueprints(app):
    from .routes import landing_bp
    from .routes import analyze_bp

    with app.app_context():
        app.register_blueprint(landing_bp)
        app.register_blueprint(analyze_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    register_blueprints(app)

    return app