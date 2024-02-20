from ddns import utils
from ddns.db import DataHandler
from ddns.exceptions import DNSRecordAlreadyExistsError
from ddns.exceptions import IdentifierTokenAlreadyExistsError

import pytest
import logging


def test_create_new_record(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )

    data = database.get_record_data(subdomain_record=test_data['subdomain_record'])
    identifier_token, secret_token = utils.unpack_api_token(test_data['api_token'])

    assert data.subdomain_record == test_data['subdomain_record']
    assert data.identifier_token == identifier_token


def test_create_existing_identifier_token(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )

    with pytest.raises(IdentifierTokenAlreadyExistsError):
        database.create_new_record(
            subdomain_record='example.com',
            api_token=test_data['api_token']
        )


def test_create_existing_dns_record(database: DataHandler, test_data: list):
    database.create_new_record(
        subdomain_record=test_data['subdomain_record'],
        api_token=test_data['api_token']
    )

    with pytest.raises(DNSRecordAlreadyExistsError):
        database.create_new_record(
            subdomain_record=test_data['subdomain_record']
        )
