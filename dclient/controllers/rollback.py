import os
import json
import falcon


def post_rollback(self, data):
    try:
        os.system("yum history rollback "+data["yum_rollback_id"])
        response_object = {
            "body": {
                "status": "success",
                "message": "Deployment successfully rolled back.",
                "data": json.dumps(data)
            },
            "status": falcon.HTTP_201
        }
        return response_object
    else:
        response_object = {
            "body": {
                "status": "fail",
                "message": "POST healthcheck failed.",
            },
            "status": falcon.HTTP_409
        }
        return response_object
