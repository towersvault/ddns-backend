from ddns.db import DataHandler
from ddns.exceptions import DNSRecordAlreadyExistsError, APITokenAlreadyExistsError

from uuid import uuid4

import pytest

import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': str(uuid4())
}

TEST_DB = 'test-ddns-db'


@pytest.fixture(scope='session', autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run."""
    # Setup
    global database
    database = DataHandler(TEST_DB)

    yield

    # Teardown
    # print(f'Tearing down {os.path.basename(__file__)}')
    # if os.path.exists(f'{TEST_DB}.sqlite'):
    #     os.remove(f'{TEST_DB}.sqlite')


def test_create_new_record():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )

    data = database.get_record_data(dns_record=TEST_DATA['dns_record'])

    assert data.dns_record == TEST_DATA['dns_record']
    assert data.api_token == TEST_DATA['api_token']


def test_create_existing_api_token():
    with pytest.raises(APITokenAlreadyExistsError):
        database.create_new_record(
            dns_record='example.com',
            api_token=TEST_DATA['api_token']
        )


def test_create_existing_dns_record():
    with pytest.raises(DNSRecordAlreadyExistsError):
        database.create_new_record(
            dns_record=TEST_DATA['dns_record']
        )
