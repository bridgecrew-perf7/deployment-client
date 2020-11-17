from dclient.util.config import Config
from dclient.util.http_helper import get_http
from dclient.util.core import install_pkgs, restart_service

import os
from flask import request
from flask import current_app as app


def post_update():
    data = request.get_json()
    app.logger.debug(f"POST UPDATE: {data}")
    try:
<<<<<<< HEAD
        payload = {"hostname": Config.HOSTNAME, "state": "UPDATING"}
=======
        headers = {"Authorization": Config.TOKEN}
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "UPDATING",
        }
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)
        for pkg in data["packages"]:
            os.system(f"sudo yum versionlock add {pkg}")
        install_pkgs(data["packages"])
        restart_service("dclient.service")
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "Update succeeded.",
            "exception": str(e),
        }
        app.logger.debug(response)
        return response, 201
    except Exception as e:
<<<<<<< HEAD
        payload = {"hostname": Config.HOSTNAME, "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILURE",
            "message": "Update failed.",
=======
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
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
            "exception": str(e),
        }
        app.logger.debug(response)
        return response, 409
