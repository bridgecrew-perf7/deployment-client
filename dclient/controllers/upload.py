import os
import subprocess
from flask import request


def post_upload():
    data = request.get_json()
    try:
        for pkg in data["versionlock"]:
            os.system("yum versionlock add "+pkg)
        response = {
            "status": "success",
            "message": "New versionlock list successfully created.",
        }
        return response, 201
    except Exception as e:
        response = {
            "status": "fail",
            "message": "POST versionlock list failed.",
            "exception": e
        }
        return response, 409