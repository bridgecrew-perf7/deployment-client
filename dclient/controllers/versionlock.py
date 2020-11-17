from dclient.util.config import Config

<<<<<<< HEAD
import os
=======
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
import re
from subprocess import check_output
from flask import current_app as app
<<<<<<< HEAD


def post_versionlock():
    data = request.get_json()
    app.logger.debug(f"POST VERSIONLOCK: {data}")
    try:
        app.logger.info("Updating Versionlock")
        for pkg in data["versionlock"]:
            app.logger.debug(f"sudo yum versionlock add {pkg}")
            stat = os.system(f"sudo yum versionlock add {pkg}")
            if stat != 0:
                raise Exception(stat)
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "New versionlock list successfully created.",
        }
        app.logger.debug(response)
        return response, 201
    except:
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "POST versionlock list failed.",
        }
        app.logger.debug(response)
        return response, 409
=======
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac


def get_versionlock():
    try:
        app.logger.info("Getting Versionlock")
        app.logger.info("check_output(['sudo', 'yum', 'versionlock', 'list'])")
        versionlock_list = []
        versionlock = check_output(["yum", "versionlock", "list"])
        versionlock = versionlock.splitlines()
        versionlock.pop(0)
        for vl in versionlock:
            vl = vl.decode("utf-8")
            z = re.match("done", vl)
            if z:
                break
            else:
                app.logger.info(vl)
                versionlock_list.append(vl)
        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "SUCCESS",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock_list,
        }
        app.logger.debug(response)
        return response, 200
    except Exception as e:
        response = {
            "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
            "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
            "port": Config.DEPLOYMENT_CLIENT_PORT,
            "version": Config.DEPLOYMENT_CLIENT_VERSION,
            "status": "FAILED",
            "message": "Failed to GET versionlock list",
            "exception": str(e)
        }
        app.logger.debug(response)
        return response, 409
