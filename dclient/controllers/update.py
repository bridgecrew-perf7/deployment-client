import os
import requests
from flask import request

from dclient.config import Config
from dclient.util import install_pkgs, restart_service


def post_update():
    data = request.get_json()
    try:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "UPDATING"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

        for pkg in data["packages"]:
            os.system("sudo yum versionlock add {}".format(pkg))
        install_pkgs(data["packages"])

        restart_service("dclient.service")
    except Exception as e:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        response = {
            "status": "failed",
            "message": "POST update failed.",
            "exception": str(e)
        }
        return response, 409
