from dclient.util.config import Config

import re
from subprocess import check_output
from flask import current_app as app


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
            "hostname": Config.HOSTNAME,
            "port": Config.PORT,
            "api_version": Config.API_VERSION,
            "status": "SUCCESS",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock_list,
        }
        return response, 200
    except Exception as e:
        response = {
            "hostname": Config.HOSTNAME,
            "port": Config.PORT,
            "api_version": Config.API_VERSION,
            "status": "FAILED",
            "message": "Failed to GET versionlock list",
            "exception": str(e)
        }
        return response, 409
