from ddns import utils
from ddns.db import DataHandler
from tests.utils import truthy, falsy

from uuid import uuid4

import os
import pytest
import logging


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
}

TEST_DB = 'test-ddns-db'


@pytest.fixture(scope='session', autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run."""
    # Setup
    logging.debug(f'TEST_DATA: {TEST_DATA}')

    global database
    database = DataHandler(TEST_DB)

    yield

    # Teardown
    # print(f'Tearing down {os.path.basename(__file__)}')
    # if os.path.exists(f'{TEST_DB}.sqlite'):
    #     os.remove(f'{TEST_DB}.sqlite')


def test_api_token():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )

    assert truthy(database.identifier_token_exists(
        api_token=TEST_DATA['api_token']
    ))
    assert falsy(database.identifier_token_exists(
        api_token=utils.generate_full_token_pair()
    ))
