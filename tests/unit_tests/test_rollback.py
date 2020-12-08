import pytest
from requests import Session

@pytest.mark.parametrize(
    "data, expected_status, expected_data, os_return_value",
    [
        (
            {
                "deployment_id": 1,
                "yum_rollback_id": 5,
                "buildall": "true",
                "versionlock": [
                    "eig-hp-core_lib-20200527-1.5299e2c.el7.noarch",
                    "eig-hp-hp_common-20200527-1.bfc6a82.el7.noarch",
                    "eig-hp-hp_web-20200929-1.e3729c0.el7.noarch",
                ],
            },
            201,
            {
                'body': {
                    'hostname': 'www0.hp.provo1.endurancemb.com',
                    'message': 'Deployment successfully rolled back.',
                    'port': '8003',
                    'protocol': 'http',
                    'status': 'SUCCESS',
                    'version': 'v1'
                }
            },
            0
        ),
        (
            {
                "deployment_id": 1,
                "versionlock": [
                    "eig-hp-core_lib-20200527-1.5299e2c.el7.noarch",
                    "eig-hp-hp_common-20200527-1.bfc6a82.el7.noarch",
                    "eig-hp-hp_web-20200929-1.e3729c0.el7.noarch",
                ],
            },
            409,
            {
                'exception': "'yum_rollback_id'",
                'hostname': 'www0.hp.provo1.endurancemb.com',
                'message': 'Rollback failed.',
                'port': '8003',
                'protocol': 'http',
                'status': 'FAILED',
                'version': 'v1'
            },
            0
        ),
(
            {
                "deployment_id": 1,
                "yum_rollback_id": 5,
                "versionlock": [
                    "eig-hp-core_lib-20200527-1.5299e2c.el7.noarch",
                    "eig-hp-hp_common-20200527-1.bfc6a82.el7.noarch",
                    "eig-hp-hp_web-20200929-1.e3729c0.el7.noarch",
                ],
            },
            409,
            {
                'exception': '1',
                'hostname': 'www0.hp.provo1.endurancemb.com',
                'message': 'Rollback failed.',
                'port': '8003',
                'protocol': 'http',
                'status': 'FAILED',
                'version': 'v1'
            },
            1
        )

    ]
)
def test_postRollback(app, mocker, data, expected_status, expected_data, os_return_value):
    mock_requests_patch = mocker.patch.object(Session, 'patch')
    mock_requests_patch.return_value.status_code = 201

    mock_requests_post = mocker.patch.object(Session, 'post')
    mock_requests_post.return_value.status_code = 201

    mock_os = mocker.patch('os.system')
    mock_os.return_value = os_return_value

    mock_subprocess = mocker.patch('subprocess.check_output')
    mock_subprocess.return_value = b'Loaded plugins: fastestmirror, versionlock\nID     | Login user               | Date and time    | Action(s)      | Altered\n-------------------------------------------------------------------------------\n     5 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |    1   \n     4 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |    1 EE\n     3 | vagrant <vagrant>        | 2020-11-19 23:43 | Install        |   36   \n     2 | vagrant <vagrant>        | 2020-11-19 23:42 | Install        |    1   \n     1 | System <unset>           | 2020-04-30 22:05 | Install        |  325   \nhistory list\n'

    mocker.patch('subprocess.Popen')

    response = app.post("/rollback", json=data)
    assert response.status_code == expected_status
    assert response.json == expected_data