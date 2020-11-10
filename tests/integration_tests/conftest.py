import pytest
import datetime
from dclient.dclient import create_app
application = create_app


@pytest.fixture(scope="module")
def base_url():
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
