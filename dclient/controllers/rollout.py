import os
import yum
import json
import falcon
import requests
from dclient.config import Config


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    yb=yum.YumBase()
    yb.setCacheDir()
    results = yb.pkgSack.returnNewestByNameArch(patterns=packages)
    for pkg in results:
        yb.install(pkg)
    yb.buildTransaction()
    yb.processTransaction()
 

def get_yum_transaction_id():
    yh=yum.history.YumHistory()
    last = yh.last()
    return last.tid


def post_rollout(self, data):
    # Post state updating
    headers = {"Authorization": Config.TOKEN}

    payload = {"hostname": data["hostname"], "state": "updating"}
    r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload, verify=False)

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
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Success", "output": "deployment was successful", "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]), headers=headers, json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "active"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload, verify=False)
        
        response_object = {
            "body": {
                "status": "success",
                "message": "Rollout successfully executed.",
            },
            "status": falcon.HTTP_201
        }
        return response_object
    except:
        # Post state error
        # Post server_history update failed
        payload = {"hostname": data["hostname"], "state": "error"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload, verify=False)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Failed", "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]), headers=headers, json=payload, verify=False)
        
        response_object = {
            "body": {
                "status": "fail",
                "message": "POST rollout failed.",
            },
            "status": falcon.HTTP_409
        }
        return response_object
