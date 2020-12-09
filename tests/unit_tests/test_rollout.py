import pytest
from requests import Session

@pytest.mark.parametrize(
    "data, expected_status, expected_data, os_return_value",
    [
        (
            {
                "deployment_id": 1,
                "versionlock": ["httpd-2.4.6-93.el7.centos.x86_64", "mod_perl-2.0.11-1.el7.x86_64"],
                "buildall": True
            },
            201,
            {
                'hostname': 'www0.hp.provo1.endurancemb.com',
                'message': 'Rollout successfully executed.',
                'port': '8003',
                'protocol': 'http',
                'status': 'SUCCESS',
                'version': 'v1',
            },
            0
        ),
        (
            {
                "deployment_id": 1,
                "versionlock": ["httpd-2.4.6-93.el7.centos.x86_64", "mod_perl-2.0.11-1.el7.x86_64"],
                "buildall": True
            },
            409,
            {
                'exception': '1',
                'hostname': 'www0.hp.provo1.endurancemb.com',
                'message': 'Rollout failed.',
                'port': '8003',
                'protocol': 'http',
                'status': 'FAILED',
                'version': 'v1'
            },
            1
        )
    ]
)
def test_postRollout(app, mocker, data, expected_status, expected_data, os_return_value):
    mock_requests_patch = mocker.patch.object(Session, 'patch')
    mock_requests_patch.return_value.status_code = 201

    mock_requests_post = mocker.patch.object(Session, 'post')
    mock_requests_post.return_value.status_code = 201

    mock_os = mocker.patch('os.system')
    mock_os.return_value = os_return_value

    mock_subprocess = mocker.patch('subprocess.check_output')
    mock_subprocess.return_value = b'Loaded plugins: fastestmirror, versionlock\nID     | Login user               | Date and time    | Action(s)      | Altered\n-------------------------------------------------------------------------------\n     5 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |    1   \n     4 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |    1 EE\n     3 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |   36   \n     2 | vagrant <vagrant>        | 2020-11-19 23:42 | Install        |    1   \n     1 | System <unset>           | 2020-04-30 22:05 | Install        |  325   \nhistory list\n'

    mocker.patch('subprocess.Popen')

    response = app.post("/rollout", json=data)

    assert response.status_code == expected_status
    assert response.json == expected_data