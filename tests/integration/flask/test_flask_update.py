from ddns import utils
from ddns.db import DataHandler


def test_record_update(ratelimit_client,
                       database: DataHandler,
                       test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'],
                               api_token=test_data['api_token'])

    res_get = ratelimit_client.get(f'/record/update?api_token={test_data["api_token"]}')
    res_post = ratelimit_client.post('/record/update',
                           data={'api_token': test_data['api_token']})

    assert res_get.status_code == 200
    assert res_post.status_code == 200


def test_record_update_wrong_identifier_token(ratelimit_client):
    api_token = utils.generate_full_token_pair()

    res_get = ratelimit_client.get(f'/record/update?api_token={api_token}')
    res_post = ratelimit_client.post('/record/update', data={'api_token': api_token})

    assert res_get.status_code == 401
    assert res_post.status_code == 401


def test_record_update_wrong_secret_token(ratelimit_client,
                                          database: DataHandler,
                                          test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'],
                               api_token=test_data['api_token'])

    identifier, secret = utils.unpack_api_token(test_data['api_token'])
    test_token = utils.generate_full_token_pair(identifier=identifier)

    res_get = ratelimit_client.get(f'/record/update?api_token={test_token}')
    res_post = ratelimit_client.post('/record/update', data={'api_token': test_token})

    assert res_get.status_code == 401
    assert res_post.status_code == 401


def test_record_update_rate_limit(client,
                                  database: DataHandler,
                                  test_data: list):
    database.create_new_record(subdomain_record=test_data['subdomain_record'],
                               api_token=test_data['api_token'])

    # Bruteforce trigger the limiter.
    for i in range(0, 10):
        r = client.get(f'/record/update?api_token={test_data["api_token"]}')
        if r.status_code == 429:
            break
    
    res_get = client.get(f'/record/update?api_token={test_data["api_token"]}')
    res_post = client.post('/record/update', 
                            data={'api_token': test_data['api_token']})
    
    assert res_get.status_code == 429
    assert res_post.status_code == 429
