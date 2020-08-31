import os
import subprocess
from flask import request


def post_versionlock():
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


def get_versionlock():
    try:
        versionlock = subprocess.check_output("yum versionlock list", shell=True)
        versionlock = versionlock.splitlines()
        versionlock.pop(0)
        versionlock.pop()
        response = {
            "status": "success",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock,
        }
        return response, 200
    except Exception as e:
        response = {
            "message": "Failed to GET versionlock list",
            "exception": e
        }
        return response, 409
