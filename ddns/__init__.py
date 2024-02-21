from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from ddns.routes import record
from ddns.routes import cli

import config
import logging
import os


logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='DDNS [%(levelname)s]: %(message)s',
    level=logging.INFO
)
logging.getLogger().addHandler(logging.StreamHandler())


def create_app(test_config=False) -> Flask:
    # Load environment variables
    load_dotenv()

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        # Load the instance config, if it exists, when not testing
        app.config.from_object(config.ProductionConfig)

        # Initialize Limiter
        limiter = Limiter(
            get_remote_address,
            app=app,
            default_limits=['10/second']
        )
        limiter.limit('2/minute')(record.blueprint)
        limiter.exempt(cli.blueprint)
    else:
        # Load the test config if passed in
        app.config.from_object(config.TestingConfig)

        # Initialize Limiter
        limiter = Limiter(
            get_remote_address,
            app=app,
            default_limits=['10/second']
        )
        limiter.limit('10/minute')(record.blueprint)
        limiter.exempt(cli.blueprint)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    app.register_blueprint(cli.blueprint)
    app.register_blueprint(record.blueprint)

    return app
