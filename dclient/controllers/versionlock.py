from dclient.util.config import Config, get_logger

import os
import re
from flask import request
from subprocess import check_output

logger = get_logger()


def post_versionlock():
    data = request.get_json()
    try:
        logger.info("Updating Versionlock")
        for pkg in data["versionlock"]:
            logger.debug(f"sudo yum versionlock add {pkg}")
            stat = os.system(f"sudo yum versionlock add {pkg}")
            if stat != 0:
                raise Exception(stat)
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
        logger.debug("Getting Versionlock")
        logger.debug("check_output(['sudo', 'yum', 'versionlock', 'list'])")
        versionlock_list = []
        versionlock = check_output(["sudo", "yum", "versionlock", "list"])
        versionlock = versionlock.splitlines()
        versionlock.pop(0)
        for vl in versionlock:
            z = re.match("done", vl)
            if z:
                break
            else:
                versionlock_list.append(vl)
        response = {
            "hostname": Config.HOSTNAME,
            "status": "SUCCESS",
            "message": "Versionlock list successfully retrieved",
            "versionlock": versionlock_list,
        }
        return response, 200
    except:
        response = {
            "hostname": Config.HOSTNAME,
            "status": "FAILED",
            "message": "Failed to GET versionlock list",
        }
        return response, 409
