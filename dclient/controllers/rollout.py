import os
from flask import request
from flask import current_app as app
from dclient.util.config import Config
from dclient.util.http_helper import get_http
from dclient.util.core import (
    get_yum_transaction_id,
    install_pkgs,
    restart_service,
    not_installed,
)


def post_rollout():
    """Post Rollout Operation

    post data:
        buildall: whether to run buildall with this operation or not
          type: boolean
          default: False
        deployment_id: the deployment_id for the deployment that issued this operation
          type: integer
          example: 1
        versionlock: an array of RPM packages to install / update
          type: array
          example: ["httpd-2.4.6-93.el7.centos.x86_64", "mod_perl-2.0.11-1.el7.x86_64"]

    :return: response
    """

    data = request.get_json()
    app.logger.debug(f"POST ROLLOUT: {data}")

<<<<<<< HEAD
    payload = {"hostname": Config.HOSTNAME, "state": "UPDATING"}
=======
    payload = {
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "state": "UPDATING",
    }
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

    try:
<<<<<<< HEAD
        for pkg in data["versionlock"]:
            stat = os.system(f"sudo yum versionlock add {pkg}")
            if stat != 0:
                raise Exception(stat)

        if not get_installed("httpd"):
            data["versionlock"].append("httpd")
        if not get_installed("mod_perl"):
            data["versionlock"].append("mod_perl")
        install_pkgs(data["versionlock"])

=======
        if "versionlock" in data:
            os.system("sudo yum versionlock clear")
            if not_installed("httpd"):
                install_pkgs(["httpd"])
            if not_installed("mod_perl"):
                install_pkgs(["mod_perl"])
            install_pkgs(data["versionlock"])
            for pkg in data["versionlock"]:
                stat = os.system(f"sudo yum versionlock add {pkg}")
                if stat != 0:
                    raise Exception(stat)
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        if data["buildall"]:
            stat = os.system("sudo /var/hp/common/bin/buildall -s")
            if stat != 0:
                raise Exception(stat)

        restart_service("httpd.service")
        stat = os.system("systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)

        payload = {
            "deployment_id": int(data["deployment_id"]),
            "action": "UPDATE",
            "state": "SUCCESS",
            "output": "deployment was successful",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        headers = {"Authorization": Config.TOKEN}
        http = get_http()
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.DEPLOYMENT_CLIENT_HOSTNAME}",
            headers=headers,
            json=payload,
        )

        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "ACTIVE",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "SUCCESS",
            "message": "Rollout successfully executed.",
        }
        return response, 201
    except Exception as e:
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "ERROR",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        payload = {
            "server_id": Config.SERVER_ID,
            "deployment_id": int(data["deployment_id"]),
            "action": "Update",
            "state": "FAILED",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        headers = {"Authorization": Config.TOKEN}
        http = get_http()
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.DEPLOYMENT_CLIENT_HOSTNAME}",
            headers=headers,
            json=payload,
        )

        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "FAILED",
            "message": "Rollout failed.",
            "exception": str(e),
        }
        return response, 409
