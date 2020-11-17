from dclient.util.config import Config
from dclient.util.http_helper import get_http
from dclient.util.core import get_yum_transaction_id, restart_service

import os
from flask import request
from flask import current_app as app



def post_rollback():
    """Post Rollback Operation

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
<<<<<<< HEAD
    app.logger.debug(data)
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": Config.HOSTNAME, "state": "UPDATING"}
=======
    app.logger.info(data)
    payload = {
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "state": "UPDATING",
    }
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_API_URI}/server", headers=headers, json=payload)

    try:
        os.system(f"yum -y history rollback {data['yum_rollback_id']}")
        if "versionlock" in data:
            for pkg in data["versionlock"]:
                os.system(f"sudo yum versionlock add {pkg}")
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
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.DEPLOYMENT_CLIENT_HOSTNAME}",
            headers=headers,
            json=payload,
        )

<<<<<<< HEAD
        payload = {"hostname": Config.HOSTNAME, "state": "ACTIVE"}
=======
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "ACTIVE",
        }
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=payload)

        response = {
            "body": {
                "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
                "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
                "port": Config.DEPLOYMENT_CLIENT_PORT,
                "version": Config.DEPLOYMENT_CLIENT_VERSION,
                "status": "SUCCESS",
                "message": "Deployment successfully rolled back.",
            },
        }
        return response, 201
    except Exception as e:
<<<<<<< HEAD
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": Config.HOSTNAME, "state": "ERROR"}
=======
        payload = {
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "state": "ERROR",
        }
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", headers=headers, json=payload)

        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1

        payload = {
<<<<<<< HEAD
            "server_id": Config.SERVER_ID,
            "deployment_id": data["deployment_id"],
            "action": "Updating RPMs",
            "state": "FAILURE",
=======
            "deployment_id": int(data["deployment_id"]),
            "action": "Update",
            "state": "FAILED",
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id,
        }
        http = get_http()
        http.post(
<<<<<<< HEAD
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.HOSTNAME}",
            headers=headers,
=======
            f"{Config.DEPLOYMENT_API_URI}/server/history/{Config.DEPLOYMENT_CLIENT_HOSTNAME}",
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
            json=payload,
        )

        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "FAILED",
            "message": "Rollback failed.",
            "exception": str(e),
        }
        return response, 409
