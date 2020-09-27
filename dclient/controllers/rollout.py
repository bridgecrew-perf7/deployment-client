import os
import requests
from flask import request
from dclient.config import Config
from dclient.util import get_yum_transaction_id, install_pkgs, restart_service


def post_rollout():
    data = request.get_json()

    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

    try:
        for pkg in data["versionlock"]:
            stat = os.system("yum versionlock add {}".format(pkg))
            if stat != 0:
                raise Exception(stat)
        install_pkgs(data["versionlock"])
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            stat = os.system("/var/hp/common/bin/buildall -s")
            if stat != 0:
                raise Exception(stat)
        restart_service("httpd.service")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)

        # Post server_history (action, yum_transaction_id, yum_rollback_id)
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "SUCCESS",
                   "output": "deployment was successful", "yum_transaction_id": yum_transaction_id,
                   "yum_rollback_id": yum_rollback_id}
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]),
                      headers=headers, json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "ACTIVE"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        
        response = {
            "status": "success",
            "message": "Rollout successfully executed.",
        }
        return response, 201
    except Exception as e:
        # Post state error
        # Post server_history update failed
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Failed",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]),
                      headers=headers, json=payload, verify=False)
        
        response = {
            "status": "FAILED",
            "message": "POST rollout failed.",
            "exception": str(e)
        }
        return response, 409

