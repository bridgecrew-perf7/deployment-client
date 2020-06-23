import os
import json
import falcon


def post_versionlock(self, data):
    try:
        os.system("yum versionlock clear")
        for pkg in data:
            os.system("yum versionlock add "+pkg)
        response_object = {
            "body": {
                "status": "success",
                "message": "New versionlock list successfully created.",
                "data": json.dumps(data)
            },
            "status": falcon.HTTP_201
        }
        return response_object
    except:
        response_object = {
            "body": {
                "status": "fail",
                "message": "POST versionlock list failed.",
            },
            "status": falcon.HTTP_409
        }
        return response_object


def get_versionlock(self):
    try:
        with open("/etc/yum/pluginconf.d/versionlock.list") as file:
            data = file.read().split(",")
        response_object = {
            "body": {
                "status": "success",
                "message": "Versionlock list successfully retrieved",
                "data": json.dumps(data),
            },
            "status": falcon.HTTP_200
        }
        return response_object
    except:
        response_object = {
            "body": {
                "message": "Failed to GET versionlock list",
            },
            "status": falcon.HTTP_409
        }
        return response_object
