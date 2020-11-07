import pytest
import datetime
from dproxy.app import app as application
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="module")
def base_url():
    url = 'http://localhost.localdomain:8003/api/v1'
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


@pytest.fixture(scope="module")
def secret_key():
    secret_key = "EnzHRohtbOd2KN3Z5VssLbG45FmlVQPLQAmJj7eFBHEPqwoHvX"
    return secret_key


@pytest.fixture()
def server_auth_cookie(app):
    claims = {
        "sub": "server",
        "aud": "deployment-api",
        "authorization": {
            "roles": ["server"],
        },
        "username": "servertester",
        "firstname": "serveradmin",
        "lastname": "tester",
        "email": "server.tester@test.com",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
        "iat": datetime.datetime.utcnow()
    }

    with app.app_context():
        access_token = create_access_token(identity="servertester", fresh=True, user_claims=claims)

    cookie = {
        "access_token_cookie": access_token
    }

    return cookie
