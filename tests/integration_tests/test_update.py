import requests


def test_post_update(base_url):
    data = {
        "packages": ["dclient"]
    }
    response = requests.post(base_url + "/update", json=data)
    print(response.text)
    assert response.status_code == 201
