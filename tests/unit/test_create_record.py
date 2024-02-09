from ddns.db import DataHandler
from ddns.exceptions import DNSRecordAlreadyExistsError, APITokenAlreadyExistsError

from uuid import uuid4

import pytest

import os


TEST_DATA = {
    'dns_record': 'test.softwxre.io',
    'api_token': 'aac90ebe-7d8c-4ad8-9d7a-68e280da3d41'
}

TEST_DB = f'test-ddns-{str(uuid4())}'


@pytest.fixture(scope='session', autouse=True)
def run_before_and_after_tests():
    """Fixture to execute asserts before and after a test is run."""
    # Setup
    global database
    database = DataHandler(TEST_DB)

    yield

    # Teardown
    print('Tearing down tests..')
    os.remove(f'{TEST_DB}.sqlite')


def truthy(value):
    return bool(value)


def falsy(value):
    return not bool(value)


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
