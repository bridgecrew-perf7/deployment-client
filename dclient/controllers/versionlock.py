from dclient.util.config import Config

import re
import subprocess
from flask import current_app as app


def get_versionlock():
    try:
        app.logger.info("Getting Versionlock")
        app.logger.info("subprocess.check_output(['sudo', 'yum', 'versionlock', 'list'])")
        versionlock_list = []
        versionlock = subprocess.check_output(["yum", "versionlock", "list"])
        versionlock = versionlock.splitlines()
        versionlock.pop(0)
        for vl in versionlock:
            vl = vl.decode("utf-8")
            z = re.search("done", vl)
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
