import os
import yum
import requests
from flask import request
from dclient.config import Config


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    yb = yum.YumBase()
    yb.setCacheDir()
    results = yb.pkgSack.returnNewestByNameArch(patterns=packages)
    for pkg in results:
        yb.install(pkg)
    yb.buildTransaction()
    yb.processTransaction()
 

def get_yum_transaction_id():
    yh = yum.history.YumHistory()
    last = yh.last()
    return last.tid


def post_rollout():
    data = request.get_json()
    # Post state updating
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

    try:
        for pkg in data["versionlock"]:
            os.system("yum versionlock add "+pkg)
        install_pkgs(data["versionlock"])
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            os.system("/var/hp/common/bin/buildall -s")
        os.system("/bin/systemctl restart httpd")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)
        
        # Post state update complete
        # Post server_history (action, yum_transaction_id, yum_rollback_id)
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Success",
                   "output": "deployment was successful", "yum_transaction_id": yum_transaction_id,
                   "yum_rollback_id": yum_rollback_id}
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]), headers=headers,
                      json=payload, verify=False)

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
        requests.post("{}/server/history/{}".format(Config.DEPLOYMENT_SERVER_URL, data["hostname"]), headers=headers,
                      json=payload, verify=False)
        
        response = {
            "status": "fail",
            "message": "POST rollout failed.",
            "exception": e
        }
        return response, 409
