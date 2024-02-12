from flask import current_app
from uuid import uuid4

from ddns import create_app
from ddns.db import DataHandler

import pytest
import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': str(uuid4())
}


@pytest.fixture(scope='session', autouse=True)
def app():
    app = create_app(test_config=True)

    # Setup
    global database
    database = DataHandler(app.config['DATABASE'])
    create_test_record()

    yield app

    # Teardown
    # print(f'Tearing down {os.path.basename(__file__)}')
    # if os.path.exists(f'{app.config["DATABASE"]}.sqlite'):
    #     os.remove(f'{app.config["DATABASE"]}.sqlite')


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def create_test_record():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )
