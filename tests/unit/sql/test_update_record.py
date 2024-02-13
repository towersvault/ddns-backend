from ddns import utils
from ddns.db import DataHandler
from ddns.exceptions import IdentifierTokenNotFoundError
from ddns.exceptions import SecretTokenIncorrectError

from uuid import uuid4

import pytest
import logging
import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
}

TEST_DB = 'test-ddns-db'

TEST_IP = '255.0.0.1'


@pytest.fixture(scope='session', autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run."""
    # Setup
    logging.debug(f'TEST_DATA: {TEST_DATA}')
    
    global database
    database = DataHandler(TEST_DB)
    create_test_record()

    yield

    # Teardown
    # print(f'Tearing down {os.path.basename(__file__)}')
    # if os.path.exists(f'{TEST_DB}.sqlite'):
    #     os.remove(f'{TEST_DB}.sqlite')


def create_test_record():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )


def test_update_record():
    database.update_record(
        api_token=TEST_DATA['api_token'],
        ip_address=TEST_IP
    )

    data = database.get_record_data(dns_record=TEST_DATA['dns_record'])

    assert data.ip_address == TEST_IP


def test_update_record_wrong_identifier_token():
    with pytest.raises(IdentifierTokenNotFoundError):
        database.update_record(
            api_token=utils.generate_full_token_pair(),
            ip_address=TEST_IP
        )


def test_update_record_wrong_secret_token():
    identifier_token, secret_token = utils.unpack_api_token(TEST_DATA['api_token'])
    test_api_token = utils.generate_full_token_pair(identifier=identifier_token)

    with pytest.raises(SecretTokenIncorrectError):
        database.update_record(
            api_token=test_api_token,
            ip_address=TEST_IP
        )
