from uuid import uuid4

from ddns import utils

import os


TEST_DATA = {
    'dns_record': f'{str(uuid4())}',
    'recommended_api_key': utils.generate_full_token_pair()
}


def test_record_create(runner):
    result = runner.invoke(args=['record', 'create-dns', TEST_DATA['dns_record']])
    full_domain_record = f'{TEST_DATA["dns_record"]}.{os.getenv("DOMAIN_NAME")}'

    print(result.output)

    assert f'"{full_domain_record}" created!' in result.output
