from dclient.config import Config

import os


def post_versionlock(data):
    try:
        for pkg in data["versionlock"]:
            os.system(f"sudo yum versionlock add {pkg}")
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "New versionlock list successfully created.",
        }
        return response, 201
    except:
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "POST versionlock list failed.",
        }
        return response, 409


def get_versionlock():
    try:
        versionlock = os.system("sudo yum versionlock list")
        versionlock = versionlock.splitlines()
        versionlock.pop(0)
        versionlock.pop()
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock,
        }
        return response, 200
    except:
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "Failed to GET versionlock list"
        }
        return response, 409
