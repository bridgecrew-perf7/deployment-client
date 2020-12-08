import pytest


@pytest.mark.parametrize(
    "expected_status, expected_data, versionlock",
    [
        (
                200,
                {
                    'protocol': 'http',
                    'hostname': 'www0.hp.provo1.endurancemb.com',
                    'port': '8003',
                    'version': 'v1',
                    'status': 'SUCCESS',
                    'message': 'Versionlock list successfully retrieved',
                    'versionlock': []
                },
                "versionlock list done"
        ),
(
                200,
                {
                    'protocol': 'http',
                    'hostname': 'www0.hp.provo1.endurancemb.com',
                    'port': '8003',
                    'version': 'v1',
                    'status': 'SUCCESS',
                    'message': 'Versionlock list successfully retrieved',
                    'versionlock': ['0:httpd-2.4.6-40.el7.centos.*']
                },
                b'Loaded plugins: fastestmirror, versionlock\n0:httpd-2.4.6-40.el7.centos.*\nversionlock list done'
        ),
        (
                409,
                {
                    'exception': 'pop from empty list',
                    'hostname': 'www0.hp.provo1.endurancemb.com',
                    'message': 'Failed to GET versionlock list',
                    'port': '8003',
                    'protocol': 'http',
                    'status': 'FAILED',
                    'version': 'v1'
                },
                ""
        )
    ]
)
def test_getVersionlock(app, mocker, expected_status, expected_data, versionlock):
    mock_requests = mocker.patch('subprocess.check_output')
    mock_requests.return_value = versionlock
    response = app.get("/versionlock")
    assert response.status_code == expected_status
    assert response.json == expected_data
