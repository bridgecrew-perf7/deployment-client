import requests


def test_post_rollback(base_url):
    data = {"status": "good"}
    response = requests.post(base_url + "/rollback", json=data)
    print(response.text)
    assert response.status_code == 201
