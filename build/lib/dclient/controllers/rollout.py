import os
import yum
import json
import falcon


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
   # try:
    install_pkgs(data["packages"])
    yum_transaction_id = get_yum_transaction_id()
    yum_rollback_id = yum_transaction_id - 1
    if "buildall" in data:
        os.system("/var/hp/common/bin/buildall -s")
    os.system("/bin/systemctl restart httpd")
    stat = os.system("/bin/systemctl status httpd.service")
    if stat != 0:
        raise Exception(stat)
    response_object = {
        "body": {
            "status": "success",
            "message": "Rollout successfully executed.",
            "yum_transaction_id": yum_transaction_id,
            "yum_rollback_id": yum_rollback_id
        },
        "status": falcon.HTTP_201
    }
    return response_object
   # except:
   #     response_object = {
   #         "body": {
   #             "status": "fail",
   #             "message": "POST rollout failed.",
   #         },
   #         "status": falcon.HTTP_409
   #     }
   #     return response_object
