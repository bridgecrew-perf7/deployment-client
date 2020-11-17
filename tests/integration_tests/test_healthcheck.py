import requests


<<<<<<< HEAD
def test_post_health_check(base_url):
    data = {"status": "good"}
    response = requests.post(base_url + "/", json=data)
    print(response.text)
    assert response.status_code == 201


=======
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
def test_get_health_check(base_url):
    response = requests.get(base_url + "/")
    print(response.text)
    assert response.status_code == 200
