from flask import Flask
from dotenv import load_dotenv

from ddns.routes import record

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
    # app.config.from_mapping(
    #     SECRET_KEY=os.getenv('FLASK_SECRET_KEY')
    # )

    if not test_config:
        # Load the instance config, if it exists, when not testing
        app.config.from_object(config.ProductionConfig)
    else:
        # Load the test config if passed in
        app.config.from_object(config.TestingConfig)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    app.register_blueprint(record.blueprint)

    return app
