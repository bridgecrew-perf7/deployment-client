import pytest
from requests import Session
from dclient.util.core import restart_service, register_dclient, update_env, set_state


@pytest.mark.parametrize(
    "expected_status, expected_data",
    [
        (201, True),
        (409, False),
        (500, False)
    ]
)
def test_set_state(mocker, expected_status, expected_data):
    mock_requests = mocker.patch.object(Session, 'patch')
    mock_requests.return_value.status_code = expected_status
    response = set_state("ACTIVE")
    assert response == expected_data



@pytest.mark.parametrize(
    "data, expected_status, expected_data",
    [
        ({
        'status': 'success',
        'message': 'Deployment Client successfully registered.',
        'token': 'token'
    }, 201, True),
        ({}, 409, False),
        ({"a": "b"}, 409, False),

    ]
)
def test_register_dclient(mocker, data, expected_status, expected_data):
    mock_requests_post = mocker.patch.object(Session, 'post')
    mock_requests_post.return_value.status_code = expected_status

    mock_requests_patch = mocker.patch.object(Session, 'patch')
    mock_requests_patch.return_value.status_code = expected_status

    mock_requests_post.return_value.json.return_value = data
    mocker.patch('dclient.util.core.set_state', return_value=True)
    response = register_dclient()
    assert response == expected_data