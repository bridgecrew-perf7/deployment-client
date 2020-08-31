import os
import subprocess
from flask import request


def post_update():
    data = request.get_json()
    try:
        for pkg in data["versionlock"]:
            os.system("yum versionlock add "+pkg)
        for pkg in data["versionlock"]:
            os.system("yum update "+pkg)
        response = {
            "status": "success",
            "message": "Update successfully applied.",
        }
        return response, 201
    except Exception as e:
        response = {
            "status": "fail",
            "message": "Update failed.",
            "exception": e
        }
        return response, 409