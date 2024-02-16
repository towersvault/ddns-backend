from uuid import uuid4

from ddns import utils

import logging


TEST_DATA = {
    'dns_record': f'{str(uuid4())}',
    'recommended_api_key': utils.generate_full_token_pair()
}


def test_record_create(runner):
    result_pass = runner.invoke(args=['record', 'create', TEST_DATA['dns_record']])
    result_fail = runner.invoke(args=['record', 'create', TEST_DATA['dns_record']])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {TEST_DATA["dns_record"]}' in result_pass.output
    assert 'already exists.' in result_fail.output


def test_record_get(runner):
    # Finds an existing DNS record
    result_pass = runner.invoke(args=['record', 'get', TEST_DATA['dns_record']])

    # Attempts to find a DNS record that doesn't exist
    result_fail = runner.invoke(args=['record', 'get', str(uuid4())])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {TEST_DATA["dns_record"]}' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output
