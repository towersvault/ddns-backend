from uuid import uuid4

from ddns import utils

import logging


TEST_DATA = {
    'subdomain_record': f'{str(uuid4())}',
    'recommended_api_key': utils.generate_full_token_pair()
}


def test_record_create(runner):
    result_pass = runner.invoke(args=['record', 
                                      'create', 
                                      TEST_DATA['subdomain_record']])
    result_fail = runner.invoke(args=['record', 
                                      'create', 
                                      TEST_DATA['subdomain_record']])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {TEST_DATA["subdomain_record"]}' in result_pass.output
    assert 'already exists.' in result_fail.output


def test_record_get(runner):
    # Finds an existing DNS record
    result_pass = runner.invoke(args=['record', 
                                      'get', 
                                      TEST_DATA['subdomain_record']])

    # Attempts to find a DNS record that doesn't exist
    result_fail = runner.invoke(args=['record', 
                                      'get', 
                                      str(uuid4())])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {TEST_DATA["subdomain_record"]}' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output


def test_record_reset_api_token(runner):
    # Updates an existing DNS record
    result_pass = runner.invoke(args=['record',
                                      'reset-api-token',
                                      TEST_DATA['subdomain_record']])
    
    # Tries to update a non-existent DNS record
    result_fail = runner.invoke(args=['record',
                                      'reset-api-token',
                                      str(uuid4())])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {TEST_DATA["subdomain_record"]}' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output


def test_record_set_ip_address(runner):
    # Updates an existing DNS record
    result_pass = runner.invoke(args=['record',
                                      'set-ip',
                                      TEST_DATA['subdomain_record'],
                                      '0.0.0.0'])
    
    # Tries to update a non-existent DNS record
    result_fail = runner.invoke(args=['record',
                                      'set-ip',
                                      str(uuid4()),
                                      '0.0.0.0'])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert 'New IP Address: 0.0.0.0' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output
