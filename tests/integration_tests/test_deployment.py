import requests


def test_post_rollout(base_url):
    data = {
        "deployment_id": 1,
        "versionlock": [
            "eig-hp-core_lib-20200527-1.5299e2c.el7.noarch",
            "eig-hp-hp_common-20200527-1.bfc6a82.el7.noarch",
            "eig-hp-hp_web-20200929-1.e3729c0.el7.noarch",
        ],
    }
    response = requests.post(base_url + "/rollout", json=data)
    print(response.text)
    assert response.status_code == 201


def test_post_rollback(base_url):
    data = {
        "deployment_id": 1,
        "yum_rollback_id": 1,
        "versionlock": [
            "eig-hp-core_lib-20200527-1.5299e2c.el7.noarch",
            "eig-hp-hp_common-20200527-1.bfc6a82.el7.noarch",
            "eig-hp-hp_web-20200929-1.e3729c0.el7.noarch",
        ],
    }
    response = requests.post(base_url + "/rollback", json=data)
    print(response.text)
    assert response.status_code == 201
