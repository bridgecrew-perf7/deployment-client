import pytest

@pytest.mark.parametrize(
    "expected_status, expected_data",
    [
        (
                200,
                {
                    "hostname": "www0.hp.provo1.endurancemb.com",
                    "status": "SUCCESS",
                    "message": "system is healthy",
                }
        )
    ]
)
def test_getHealthCheck(app, expected_status, expected_data):
    response = app.get("/")
    assert response.status_code == expected_status
    if response.status_code == 200:
        assert response.json == expected_data