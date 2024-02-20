from typing import Iterator
from uuid import uuid4

from ddns import create_app
from ddns import utils
from ddns.db import DataHandler

from click.testing import Result

from pytest import CaptureFixture

from flask.testing import FlaskCliRunner

import pytest
import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
}

TEST_DB = 'ddns-test-db'


@pytest.fixture(scope='session', autouse=True)
def app():
    app = create_app(test_config=True)

    global TEST_DB
    TEST_DB = app.config['DATABASE']

    # Setup
    global database
    database = DataHandler(app.config['DATABASE'])
    create_test_record()

    yield app

    # Teardown
    print(f'Tearing down {os.path.basename(__file__)}')
    if os.path.exists(f'{app.config["DATABASE"]}.sqlite'):
        os.remove(f'{app.config["DATABASE"]}.sqlite')


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app, capsys: CaptureFixture[str]):
    class TestFlaskCliRunner(FlaskCliRunner):
        def invoke(self, *args, **kwargs) -> Result:
            with capsys.disabled():
                result = super().invoke(cli=self.app.cli, *args, **kwargs)
            return result
    
    yield TestFlaskCliRunner(app)


def create_test_record():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )
