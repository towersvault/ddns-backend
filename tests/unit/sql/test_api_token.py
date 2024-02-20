from ddns import utils
from ddns.db import DataHandler
from tests.utils import truthy, falsy
from ddns.exceptions import IdentifierTokenNotFoundError
from ddns.exceptions import SecretTokenIncorrectError

import pytest


def test_api_token(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )
    incorrect_api_token = utils.generate_full_token_pair()

    assert truthy(database.identifier_token_exists(
        api_token=test_data['api_token']
    ))
    assert falsy(database.identifier_token_exists(
        api_token=incorrect_api_token
    ))


def test_get_bound_dns(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )

    bound_dns_record = database.get_bound_subdomain_record(test_data['api_token'])
    assert bound_dns_record == test_data['subdomain_record']


def test_get_bound_dns_incorrect_api_token(database: DataHandler):
    incorrect_token = utils.generate_full_token_pair()

    with pytest.raises(IdentifierTokenNotFoundError):
        database.get_bound_subdomain_record(incorrect_token)


def test_get_bound_dns_incorrect_secret_token(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )

    identifier_token, secret_token = utils.unpack_api_token(test_data['api_token'])
    new_test_token = utils.generate_full_token_pair(identifier=identifier_token)

    with pytest.raises(SecretTokenIncorrectError):
        database.get_bound_subdomain_record(new_test_token)
