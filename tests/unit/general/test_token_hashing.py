from ddns import utils
from tests.utils import truthy, falsy


def test_hash_match():
    secret_token = utils.generate_secret_token()
    hashed_secret_token = utils.hash_token(secret_token)

    other_secret_token = utils.generate_secret_token()
    other_hashed_secret_token = utils.hash_token(other_secret_token)

    assert truthy(utils.check_hashed_token(
        token=secret_token,
        hashed_token=hashed_secret_token
    ))
    assert falsy(utils.check_hashed_token(
        token=secret_token,
        hashed_token=other_hashed_secret_token
    ))