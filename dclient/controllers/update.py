import requests
from flask import request

from dclient.config import Config
from dclient.util import sudo_cmd, install_pkgs, restart_service


def post_update():
    data = request.get_json()
    try:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "updating"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

        for pkg in data["packages"]:
            sudo_cmd("yum versionlock add {}".format(pkg), verbose=False)
        install_pkgs(data["packages"])

        restart_service("dclient.service")
        stat = sudo_cmd("/bin/systemctl status dclient.service", verbose=False)
        if stat != 0:
            raise Exception(stat)

        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "active"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

        response = {
            "status": "success",
            "message": "Update successfully executed.",
        }
        return response, 201
    except Exception as e:
        payload = {"hostname": data["hostname"], "state": "error"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        response = {
            "status": "failed",
            "message": "POST update failed.",
            "exception": str(e)
        }
        return response, 409
