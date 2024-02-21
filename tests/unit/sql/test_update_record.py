from ddns import utils
from ddns.db import DataHandler
from ddns.exceptions import DNSRecordNotFoundError

from uuid import uuid4

import pytest

TEST_IP = '255.0.0.1'


def test_update_record(database: DataHandler, test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'],
                               api_token=test_data['api_token'])

    database.update_record_ip_address(
        subdomain_record=test_data['subdomain_record'],
        ip_address=TEST_IP)

    data = database.get_record_data(
        subdomain_record=test_data['subdomain_record'])

    assert data.ip_address == TEST_IP


def test_update_record_wrong_dns_record(database: DataHandler):
    with pytest.raises(DNSRecordNotFoundError):
        database.update_record_ip_address(
            subdomain_record=f'test-{str(uuid4())}',
            ip_address=TEST_IP)


def test_update_record_new_api_token(database: DataHandler, test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'],
                               api_token=test_data['api_token'])

    new_api_token = database.update_record_api_token(
        test_data['subdomain_record'])

    test_api_token = utils.generate_full_token_pair()
    return_api_token = database.update_record_api_token(
        subdomain_record=test_data['subdomain_record'],
        new_api_token=test_api_token
    )

    assert len(new_api_token) == utils.TOTAL_TOKEN_LENGTH
    assert test_api_token == return_api_token


def test_update_record_new_api_token_incorrect_dns(database: DataHandler):
    with pytest.raises(DNSRecordNotFoundError):
        database.update_record_api_token(
            subdomain_record=f'test-{str(uuid4())}'
        )
