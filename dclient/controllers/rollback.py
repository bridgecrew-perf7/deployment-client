from dclient.util.config import Config
from flask import current_app as app
from dclient.util.http_helper import get_http
from dclient.util.core import get_yum_transaction_id, restart_service

import os
from flask import request


def post_rollback():
    """ Post Rollback Operation

    post data
        buildall:
          type: boolean
          default: False
        deployment_id:
          type: integer
          example: 1
        versionlock:
          type: array
          example: ["httpd-2.4.6-93.el7.centos.x86_64", "mod_perl-2.0.11-1.el7.x86_64"]
        yum_rollback_id:
          type: integer
          example: 10
    :return: response
    """

    data = request.get_json()
    app.logger.debug(data)
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": Config.HOSTNAME, "state": "UPDATING"}
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_API_URI}/server", headers=headers, json=payload)

    try:
        os.system(f"yum -y history rollback {data['yum_rollback_id']}")
        for pkg in data["versionlock"]:
            os.system(f"yum versionlock add {pkg}")
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        if data["buildall"]:
            os.system("sudo /var/hp/common/bin/buildall -s")

        restart_service("httpd.service")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)

        payload = {
            "server_id": Config.SERVER_ID,
            "deployment_id": data["deployment_id"],
            "action": "UPDATE",
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

        payload = {"hostname": Config.HOSTNAME, "state": "ACTIVE"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        response = {
            "body": {
                "hostname": Config.HOSTNAME,
                "status": "SUCCESS",
                "message": "Deployment successfully rolled back.",
            },
        }
        return response, 201
    except Exception as e:
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": Config.HOSTNAME, "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", headers=headers, json=payload)

        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        payload = {
            "server_id": Config.SERVER_ID,
            "deployment_id": data["deployment_id"],
            "action": "Updating RPMs",
            "state": "FAILURE",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        http = get_http()
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.HOSTNAME}",
            headers=headers,
            json=payload,
        )

        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "Rollback failed.",
            "exception": str(e),
        }
        return response, 409
