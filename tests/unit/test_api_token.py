from ddns.db import DataHandler

from uuid import uuid4

import os
import pytest


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
    os.remove(f'{TEST_DB}.sqlite')


def truthy(value):
    return bool(value)


def falsy(value):
    return not bool(value)


def test_api_token():
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )

    assert truthy(database.api_token_exists(
        api_token=TEST_DATA['api_token']
    ))
    assert falsy(database.api_token_exists(
        api_token='5804eefa-b388-41e8-99dnotavalidtoken'
    ))
