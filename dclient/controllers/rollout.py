import os
from flask import request
from dclient.util import Config, get_http, get_yum_transaction_id, install_pkgs, restart_service, get_installed


def post_rollout():
    data = request.get_json()

    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "UPDATING"}
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)

    try:
        for pkg in data["versionlock"]:
            stat = os.system(f"sudo yum versionlock add {pkg}")
            if stat != 0:
                raise Exception(stat)
        if not get_installed("httpd"):
            data["versionlock"].append("httpd")
        if not get_installed("mod_perl"):
            data["versionlock"].append("mod_perl")
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

        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "SUCCESS",
                   "output": "deployment was successful", "yum_transaction_id": yum_transaction_id,
                   "yum_rollback_id": yum_rollback_id}
        http = get_http()
        http.post(f"{Config.DEPLOYMENT_SERVER_URL}/server/history/{data['hostname']}", headers=headers,
                      json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "ACTIVE"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)
        
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "Rollout successfully executed.",
        }
        return response, 201
    except Exception as e:
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "FAILED",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        http = get_http()
        http.post(f"{Config.DEPLOYMENT_SERVER_URL}/server/history/{data['hostname']}", headers=headers,
                      json=payload)
        
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "POST rollout failed.",
            "exception": str(e)
        }
        return response, 409

