import requests


def test_post_health_check(base_url):
    data = {"status": "good"}
    response = requests.post(base_url + "/", json=data)
    print(response.text)
    assert response.status_code == 201


def test_get_health_check(base_url):
    response = requests.get(base_url + "/")
    print(response.text)
    assert response.status_code == 200
