from uuid import uuid4

from ddns import create_app
from ddns import utils
from ddns.db import DataHandler

from config import TestingConfig

from click.testing import Result

from pytest import CaptureFixture

from flask.testing import FlaskCliRunner

import pytest


@pytest.fixture(scope='module', autouse=True)
def app():
    app = create_app(test_config=True)

    yield app


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


@pytest.fixture(scope='module')
def database():
    return DataHandler(TestingConfig.DATABASE)


@pytest.fixture(scope='function')
def test_data():
    return {
        'subdomain_record': f'test-{uuid4()}',
        'api_token': utils.generate_full_token_pair()
    }
