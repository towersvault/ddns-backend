from typing import Iterator
from flask import current_app
from uuid import uuid4

from ddns import create_app
from ddns import utils
from ddns.db import DataHandler

from click.testing import CliRunner
from click.testing import Result
from click import BaseCommand

from pytest import CaptureFixture

import pytest
import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
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


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


@pytest.fixture
def runner(capsys: CaptureFixture[str]) -> Iterator[CliRunner]:
    class TestCliRunner(CliRunner):
        def invoke(self, *args, **kwargs) -> Result:
            with capsys.disabled():
                result = super().invoke(cli=BaseCommand(name='flask'), *args, **kwargs)
            return result
    
    yield TestCliRunner()


def create_test_record():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )
