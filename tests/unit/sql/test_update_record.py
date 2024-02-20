from ddns import utils
from ddns.db import DataHandler
from ddns.exceptions import DNSRecordNotFoundError

from uuid import uuid4

import pytest
import logging
import os


TEST_DATA = {
    'dns_record': f'test.{str(uuid4())[:4]}.softwxre.io',
    'api_token': utils.generate_full_token_pair()
}

TEST_IP = '255.0.0.1'


def create_test_record(database: DataHandler):
    database.create_new_record(
        dns_record=TEST_DATA['dns_record'],
        api_token=TEST_DATA['api_token']
    )


def test_update_record(database: DataHandler):
    create_test_record(database)

    database.update_record_ip_address(
        dns_record=TEST_DATA['dns_record'],
        ip_address=TEST_IP
    )

    data = database.get_record_data(dns_record=TEST_DATA['dns_record'])

    assert data.ip_address == TEST_IP


def test_update_record_wrong_dns_record(database: DataHandler):
    with pytest.raises(DNSRecordNotFoundError):
        database.update_record_ip_address(
            dns_record=f'test.{str(uuid4())}.softwxre.io',
            ip_address=TEST_IP
        )


def test_update_record_new_api_token(database: DataHandler):
    new_api_token = database.update_record_api_token(TEST_DATA['dns_record'])

    test_api_token = utils.generate_full_token_pair()
    return_api_token = database.update_record_api_token(
        dns_record=TEST_DATA['dns_record'],
        new_api_token=test_api_token
    )

    assert len(new_api_token) == utils.TOTAL_TOKEN_LENGTH
    assert test_api_token == return_api_token


def test_update_record_new_api_token_incorrect_dns(database: DataHandler):
    with pytest.raises(DNSRecordNotFoundError):
        database.update_record_api_token(
            dns_record=f'test.{str(uuid4())}.softwxre.io'
        )
    


