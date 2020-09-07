import requests
from flask import request
from dclient.config import Config
from dclient.util import get_yum_transaction_id, sudo_cmd, install_pkgs, restart_service


def post_rollout():
    data = request.get_json()

    # Post state updating
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

    try:
        for pkg in data["versionlock"]:
            stat = sudo_cmd("yum versionlock add {}".format(pkg), verbose=False)
            if stat != 0:
                raise Exception(stat)
        install_pkgs(data["versionlock"])
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            stat = sudo_cmd("/var/hp/common/bin/buildall -s", verbose=False)
            if stat != 0:
                raise Exception(stat)
        restart_service("httpd.service")
        stat = sudo_cmd("/bin/systemctl status httpd.service", verbose=False)
        if stat != 0:
            raise Exception(stat)

        # Post server_history (action, yum_transaction_id, yum_rollback_id)
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Success",
                   "output": "deployment was successful", "yum_transaction_id": yum_transaction_id,
                   "yum_rollback_id": yum_rollback_id}
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]),
                      headers=headers, json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "active"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        
        response = {
            "status": "success",
            "message": "Rollout successfully executed.",
        }
        return response, 201
    except Exception as e:
        # Post state error
        # Post server_history update failed
        payload = {"hostname": data["hostname"], "state": "error"}
        requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Failed",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]),
                      headers=headers, json=payload, verify=False)
        
        response = {
            "status": "failed",
            "message": "POST rollout failed.",
            "exception": str(e)
        }
        return response, 409

