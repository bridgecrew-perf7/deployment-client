from dclient.util.config import Config
from dclient.util.http_helper import get_http
from dclient.util.core import install_pkgs, restart_service

import os
from flask import request


def post_update():
    data = request.get_json()
    try:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "UPDATING"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        for pkg in data["packages"]:
            os.system(f"sudo yum versionlock add {pkg}")
        install_pkgs(data["packages"])

        restart_service("dclient.service")
    except Exception as e:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "POST update failed.",
            "exception": str(e)
        }
        return response, 409
