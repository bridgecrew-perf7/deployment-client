from dclient.util.config import Config
from dclient.util.http_helper import get_http
from dclient.util.core import install_pkgs, restart_service

import os
from flask import request


def post_update():
    data = request.get_json()
    try:
        headers = {"Authorization": Config.TOKEN}
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "UPDATING",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)
        for pkg in data["packages"]:
            os.system(f"sudo yum versionlock add {pkg}")
        install_pkgs(data["packages"])
        restart_service("dclient.service")
    except Exception as e:
        headers = {"Authorization": Config.TOKEN}
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "ERROR",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)
        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "FAILED",
            "message": "POST update failed.",
            "exception": str(e),
        }
        return response, 409
