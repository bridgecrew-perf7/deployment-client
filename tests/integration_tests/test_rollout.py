import requests


def test_post_rollout(base_url):
    data = {"status": "good"}
    response = requests.post(base_url + "/rollout", json=data)
    print(response.text)
    assert response.status_code == 201
