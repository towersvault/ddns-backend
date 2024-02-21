from uuid import uuid4

from ddns.db import DataHandler

import logging


def test_record_create(runner, 
                       test_data: list):
    result_pass = runner.invoke(args=['record', 
                                      'create', 
                                      test_data['subdomain_record']])
    result_fail = runner.invoke(args=['record', 
                                      'create', 
                                      test_data['subdomain_record']])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {test_data["subdomain_record"]}' in result_pass.output
    assert 'already exists.' in result_fail.output


def test_record_get(runner, 
                    database: DataHandler,
                    test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'], 
                               api_token=test_data['api_token'])

    # Finds an existing DNS record
    result_pass = runner.invoke(args=['record', 
                                      'get', 
                                      test_data['subdomain_record']])

    # Attempts to find a DNS record that doesn't exist
    result_fail = runner.invoke(args=['record', 
                                      'get', 
                                      str(uuid4())])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {test_data["subdomain_record"]}' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output


def test_record_reset_api_token(runner, 
                                database: DataHandler, 
                                test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'], 
                               api_token=test_data['api_token'])

    # Updates an existing DNS record
    result_pass = runner.invoke(args=['record',
                                      'reset-api-token',
                                      test_data['subdomain_record']])
    
    # Tries to update a non-existent DNS record
    result_fail = runner.invoke(args=['record',
                                      'reset-api-token',
                                      str(uuid4())])

    logging.debug(f'Result Pass: {result_pass.output}')
    logging.debug(f'Result Fail: {result_fail.output}')

    assert f'DNS Record: {test_data["subdomain_record"]}' in result_pass.output
    assert 'doesn\'t exist.' in result_fail.output


def test_record_set_ip_address(runner, 
                               database: DataHandler, 
                               test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'], 
                               api_token=test_data['api_token'])

    # Updates an existing DNS record
    result_pass = runner.invoke(args=['record',
                                      'set-ip',
                                      test_data['subdomain_record'],
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
