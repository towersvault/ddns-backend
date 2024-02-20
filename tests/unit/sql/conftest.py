from config import TestingConfig
from ddns.db import DataHandler
from ddns.utils import generate_full_token_pair

from uuid import uuid4

import pytest


@pytest.fixture(scope='module')
def database():
    return DataHandler(TestingConfig.DATABASE)


@pytest.fixture(scope='module')
def test_data():
    return {
        'subdomain_record': f'test-{uuid4()}',
        'api_token': generate_full_token_pair()
    }
