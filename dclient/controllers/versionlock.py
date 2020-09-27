import os


def post_versionlock(data):
    try:
        for pkg in data["versionlock"]:
            os.system("sudo yum versionlock add {}".format(pkg))
        response = {
            "status": "success",
            "message": "New versionlock list successfully created.",
        }
        return response, 201
    except:
        response = {
            "status": "fail",
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
            "status": "success",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock,
        }
        return response, 200
    except:
        response = {
            "status": "failure",
            "message": "Failed to GET versionlock list"
        }
        return response, 409
