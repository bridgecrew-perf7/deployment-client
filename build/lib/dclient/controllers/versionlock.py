import os
import json
import falcon
import subprocess

def post_versionlock(self, data):
    try:
        os.system("yum versionlock clear")
        for pkg in data:
            os.system("yum versionlock add "+pkg)
        response_object = {
            "body": {
                "status": "success",
                "message": "New versionlock list successfully created.",
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
    #try:
    versionlock = subprocess.check_output("yum versionlock list", shell=True)
    versionlock = versionlock.splitlines()
    versionlock.pop(0)
    versionlock.pop()
    response_object = {
        "body": {
            "status": "success",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock,
        },
        "status": falcon.HTTP_200
    }
    return response_object
   # except:
   #     response_object = {
   #         "body": {
   #             "message": "Failed to GET versionlock list",
   #         },
   #         "status": falcon.HTTP_409
   #     }
   #     return response_object
