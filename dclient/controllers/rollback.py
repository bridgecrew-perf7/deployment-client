from dclient.util.config import Config
from flask import current_app as app
from dclient.util.http_helper import get_http
from dclient.util.core import get_yum_transaction_id, restart_service

import os
from flask import request


def post_rollback():
    data = request.get_json()
    app.logger.info(data)
    headers = {"Authorization": Config.TOKEN}
    payload = {
        "hostname": data["hostname"],
        "port": data["port"],
        "api_version": data["api_version"],
        "state": "UPDATING",
    }
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

    try:
        os.system(f"yum -y history rollback {data['yum_rollback_id']}")
        for pkg in data["versionlock"]:
            os.system(f"yum versionlock add {pkg}")
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            os.system("sudo /var/hp/common/bin/buildall -s")
        restart_service("httpd.service")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)

        payload = {
            "deployment_id": data["deployment_id"],
            "action": "Update",
            "state": "SUCCESS",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        http = get_http()
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history/{data['hostname']}",
            headers=headers,
            json=payload,
        )

        payload = {
            "hostname": data["hostname"],
            "port": data["port"],
            "api_version": data["api_version"],
            "state": "ACTIVE",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        response = {
            "body": {
                "hostname": Config.HOSTNAME,
                "port": Config.PORT,
                "api_version": Config.API_VERSION,
                "status": "SUCCESS",
                "message": "Deployment successfully rolled back.",
            },
        }
        return response, 201
    except Exception as e:
        payload = {
            "hostname": data["hostname"],
            "port": data["port"],
            "api_version": data["api_version"],
            "state": "ERROR",
        }
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        payload = {
            "deployment_id": data["deployment_id"],
            "action": "Update",
            "state": "FAILED",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        http = get_http()
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history/{data['hostname']}",
            json=payload,
        )

        response = {
            "hostname": Config.HOSTNAME,
            "port": Config.PORT,
            "api_version": Config.API_VERSION,
            "status": "FAILED",
            "message": "Deployment rollback failed.",
            "exception": str(e),
        }
        return response, 409
