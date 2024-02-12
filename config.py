from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv('FLASK_PROD_SECRET_KEY')
    FLASK_SECRET = SECRET_KEY
    DATABASE = 'test-ddns-db'
    TESTING = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DATABASE = 'ddns-db'


class TestingConfig(Config):
    SECRET_KEY = os.getenv('FLASK_TEST_SECRET_KEY')
