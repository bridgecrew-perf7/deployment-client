import pytest
<<<<<<< HEAD
import datetime
from dclient.dclient import create_app
application = create_app
=======
import requests
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac


@pytest.fixture(scope="module")
def base_url():
<<<<<<< HEAD
    url = 'http://www-test.unifiedlayer.com:8003/api/v1'
    return url


@pytest.fixture
def app():
    ctx = application.app_context()
    ctx.push()
    return application


@pytest.fixture
def app_context():
    return application.app_context()


@pytest.fixture(scope="module")
def proxy_url():
    url = 'http://localhost.localdomain:8002/api/1.0.0'
    return url
=======
    url = 'http://deployment-client.com:8003'
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
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
