from ddns import utils
from ddns.db import DataHandler
from tests.utils import truthy, falsy
from ddns.exceptions import IdentifierTokenNotFoundError
from ddns.exceptions import SecretTokenIncorrectError

from uuid import uuid4

import pytest


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
}


def test_api_token(database: DataHandler):
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


def test_get_bound_dns(database: DataHandler):
    bound_dns_record = database.get_bound_dns_record(TEST_DATA['api_token'])
    assert bound_dns_record == TEST_DATA['dns_record']


def test_get_bound_dns_incorrect_api_token(database: DataHandler):
    incorrect_token = utils.generate_full_token_pair()

    with pytest.raises(IdentifierTokenNotFoundError):
        database.get_bound_dns_record(incorrect_token)


def test_get_bound_dns_incorrect_secret_token(database: DataHandler):
    identifier_token, secret_token = utils.unpack_api_token(TEST_DATA['api_token'])
    new_test_token = utils.generate_full_token_pair(identifier=identifier_token)

    with pytest.raises(SecretTokenIncorrectError):
        database.get_bound_dns_record(new_test_token)
