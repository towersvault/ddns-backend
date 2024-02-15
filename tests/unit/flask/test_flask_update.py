from .conftest import TEST_DATA

from ddns import utils


def test_record_update(client):
    res_get = client.get(f'/record/update?api_token={TEST_DATA["api_token"]}')
    res_post = client.post('/record/update', data={'api_token': TEST_DATA['api_token']})

    assert res_get.status_code == 200
    assert res_post.status_code == 200


def test_record_update_wrong_identifier_token(client):
    api_token = utils.generate_full_token_pair()

    res_get = client.get(f'/record/update?api_token={api_token}')
    res_post = client.post('/record/update', data={'api_token': api_token})

    assert res_get.status_code == 401
    assert res_post.status_code == 401


def test_record_update_wrong_secret_token(client):
    identifier, secret = utils.unpack_api_token(TEST_DATA['api_token'])
    test_token = utils.generate_full_token_pair(identifier=identifier)

    res_get = client.get(f'/record/update?api_token={test_token}')
    res_post = client.post('/record/update', data={'api_token': test_token})

    assert res_get.status_code == 401
    assert res_post.status_code == 401
