import yum
import json
import falcon


def install_pkgs(data):
    yb=yum.YumBase()
    searchlist=["name"]
    arg=data["packages"]
    matches = yb.searchGenerator(searchlist, arg)
    for (package, matched_value) in matches:
        yb.install(package)
    yb.buildTransaction()
    yb.processTransaction()


def get_yum_transaction_id():
    yh=yum.history.YumHistory()
    last = yh.last()
    return last.tid


def post_rollout(self, data):
    try:
        install_pkgs(data)
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
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
    except:
        response_object = {
            "body": {
                "status": "fail",
                "message": "POST rollout failed.",
            },
            "status": falcon.HTTP_409
        }
        return response_object
