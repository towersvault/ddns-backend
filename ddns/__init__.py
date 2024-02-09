import os

from flask import Flask
from dotenv import load_dotenv

from .routes import record


def create_app(test_config=None) -> Flask:
    # Load environment variables
    load_dotenv()

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    app.register_blueprint(record.blueprint)

    return app