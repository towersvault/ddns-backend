from uuid import uuid4

from ddns import create_app
from ddns import utils
from ddns.db import DataHandler

from config import TestingConfig

from click.testing import Result

from pytest import CaptureFixture

from flask.testing import FlaskCliRunner
from flask.testing import FlaskClient

import pytest
import time
import logging


@pytest.fixture(scope='module', autouse=True)
def app():
    app = create_app(test_config=True)

    yield app


@pytest.fixture()
def client(app):
    """Non-rate limited client.

    Use is intended for testing flask-limiter.
    """

    return app.test_client()


@pytest.fixture()
def ratelimit_client(app):
    """Rate limited client to not trigger flask-limiter."""

    class TestFlaskClient(FlaskClient):
        def get(self, *args, **kwargs) -> Result:
            """Overidden FlaskClient.get

            Handles getting rate limited (HTTP-Error 429) gracefully by waiting
            then retrying.
            """

            result = super().get(*args, **kwargs)
            while result.status_code == 429:
                logging.debug(
                    'FlaskClient-GET rate limited, sleeping for 5 seconds.')

                time.sleep(5)
                result = super().get(*args, **kwargs)

            return result

        def post(self, *args, **kwargs) -> Result:
            """Overidden FlaskClient.post

            Handles getting rate limited (HTTP-Error 429) gracefully by waiting
            then retrying.
            """

            result = super().post(*args, **kwargs)
            while result.status_code == 429:
                logging.debug(
                    'FlaskClient-POST rate limited, sleeping for 5 seconds.')

                time.sleep(5)
                result = super().post(*args, **kwargs)

            return result

    yield TestFlaskClient(app)


@pytest.fixture
def runner(app, capsys: CaptureFixture[str]):
    class TestFlaskCliRunner(FlaskCliRunner):
        def invoke(self, *args, **kwargs) -> Result:
            with capsys.disabled():
                result = super().invoke(cli=self.app.cli, *args, **kwargs)
            return result

    yield TestFlaskCliRunner(app)


@pytest.fixture(scope='module')
def database():
    return DataHandler(TestingConfig.DATABASE)


@pytest.fixture(scope='function')
def test_data():
    return {
        'subdomain_record': f'test-{uuid4()}',
        'api_token': utils.generate_full_token_pair()
    }
