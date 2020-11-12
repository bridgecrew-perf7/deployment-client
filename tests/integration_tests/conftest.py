import pytest
import requests


@pytest.fixture(scope="module")
def base_url():
    url = 'http://www-test.unifiedlayer.com:8003'
    return url


@pytest.fixture(scope="module")
def proxy_url():
    url = 'http://localhost.localdomain:8002/api/v1'
    return url


@pytest.fixture(scope="module")
def get_yum_id(base_url):
    r = requests.get(f"{base_url}/yumid")
    yum_id = r.json
    return yum_id
