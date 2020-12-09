import pytest
from unittest import mock
import os
from requests import Session
from pathlib import Path

from dclient.dclient import create_app


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ,
            {"TESTING": "1",
             "SECRET_KEY": "EnzHRohtbOd2KN3Z5VssLbG45FmlVQPLQAmJj7eFBHEPqwoHvX",
             "STATE": "ACTIVE",
             "HOSTNAME": "deployment-client.com",
             "IP": "127.0.0.1",
             "PORT": "8003",
             "PROTOCOL": "http",
             "VERSION": "v1",
             "LOCATION": "Provo",
             "ENVIRONMENT": "ALPHA",
             "DEPLOYMENT_PROXY_HOSTNAME": "deployment-proxy.unifiedlayer.com",
             "DEPLOYMENT_PROXY_PORT": "8002",
             "DEPLOYMENT_PROXY_PROTOCOL": "http",
             "DEPLOYMENT_PROXY_VERSION": "v1",
             "DEPLOYMENT_API_URI": "http://deployment-proxy.unifiedlayer.com:8002/api/v1"
            }):
        yield

@pytest.fixture(scope="module")
def app():
    application = create_app()
    client = application.test_client()
    ctx = application.app_context()
    ctx.push()
    yield client
    ctx.pop()

def pytest_sessionfinish(session, exitstatus):
    env_files = ['.env', '/etc/default/dclient']
    for env_file in env_files:
        file = Path(env_file)
        if file.is_file():
            with open(env_file) as f:
                lines = f.readlines()
            with open(env_file, "w") as f:
                for line in lines:
                    if line.strip("\n") != "TOKEN=token":
                        f.write(line)