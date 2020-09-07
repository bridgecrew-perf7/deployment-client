from dclient.util import sudo_cmd


def post_versionlock(data):
    try:
        for pkg in data["versionlock"]:
            sudo_cmd("yum versionlock add {}".format(pkg), verbose=False)
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
        versionlock = sudo_cmd("yum versionlock list", verbose=True)
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
