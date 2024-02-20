from config import TestingConfig

import pytest
import os
import logging


@pytest.fixture(scope='session', autouse=True)
def cleanup():
    yield

    logging.info('Tearing down testing')
    if os.path.exists(f'{TestingConfig.DATABASE}.sqlite'):
        os.remove(f'{TestingConfig.DATABASE}.sqlite')
