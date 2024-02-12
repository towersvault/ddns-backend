from uuid import uuid4

from .conftest import TEST_DATA


def test_record_update(client):
    res_get = client.get(f'/record/update?api_token={TEST_DATA["api_token"]}')
    res_post = client.post('/record/update', data={'api_token': TEST_DATA['api_token']})

    assert res_get.status_code == 200
    assert res_post.status_code == 200


def test_record_update_wrong_api_token(client):
    res_get = client.get(f'/record/update?api_token={str(uuid4())}')
    res_post = client.post('/record/update', data={'api_token': str(uuid4())})

    assert res_get.status_code == 401
    assert res_post.status_code == 401
