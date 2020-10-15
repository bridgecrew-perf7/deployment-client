import os
from flask import request

from dclient.config import Config
from dclient.util import install_pkgs, restart_service, get_http


def post_update():
    data = request.get_json()
    try:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "UPDATING"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)

        for pkg in data["packages"]:
            os.system(f"sudo yum versionlock add {pkg}")
        install_pkgs(data["packages"])

        restart_service("dclient.service")
    except Exception as e:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "POST update failed.",
            "exception": str(e)
        }
        return response, 409
