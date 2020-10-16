import os
from flask import request

from dclient.util import Config, get_logger, get_http, get_yum_transaction_id, restart_service

logger = get_logger()


def post_rollback():
    data = request.get_json()
    logger.info(data)
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "UPDATING"}
    http = get_http()
    http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)
    
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

        payload = {"deployment_id": data["deployment_id"], "action": "Update", "state": "SUCCESS",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        http = get_http()
        http.post(f"{Config.DEPLOYMENT_SERVER_URL}/server/history/{data['hostname']}", headers=headers,
                      json=payload)

        payload = {"hostname": data["hostname"], "state": "ACTIVE"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)

        response = {
            "body": {
                "hostname": Config.HOSTNAME,
                "status": "SUCCESS",
                "message": "Deployment successfully rolled back.",
            },
        }
        return response, 201
    except Exception as e:
        payload = {"hostname": data["hostname"], "state": "ERROR"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        
        payload = {"deployment_id": data["deployment_id"], "action": "Update", "state": "FAILED",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        http = get_http()
        http.post(f"{Config.DEPLOYMENT_SERVER_URL}/server/history/{data['hostname']}", headers=headers,
                      json=payload)
        
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "Deployment rollback failed.",
            "exception": str(e)
        }
        return response, 409

