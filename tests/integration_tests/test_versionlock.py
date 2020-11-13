import requests


def test_get_versionlock(base_url):
    response = requests.get(base_url + "/versionlock")
    print(response.text)
    assert response.status_code == 200
