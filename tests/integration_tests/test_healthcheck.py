import requests


def test_get_health_check(base_url):
    response = requests.get(base_url + "/")
    print(response.text)
    assert response.status_code == 200
