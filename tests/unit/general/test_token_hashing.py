from ddns import utils
from tests.utils import truthy
from tests.utils import falsy


def test_hash_match():
    secret_token = utils.generate_secret_token()
    hashed_secret_token = utils.hash_token(secret_token)

    other_secret_token = utils.generate_secret_token()
    other_hashed_secret_token = utils.hash_token(other_secret_token)

    assert truthy(utils.compare_hashed_token(secret_token=secret_token,
                                             hashed_secret_token=hashed_secret_token))
    assert falsy(
        utils.compare_hashed_token(
            secret_token=secret_token,
            hashed_secret_token=other_hashed_secret_token))
