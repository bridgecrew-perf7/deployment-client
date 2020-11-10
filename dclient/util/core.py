from dclient.util.config import Config, get_var
from dclient.util.http_helper import get_http

import os
import re
from dotenv import load_dotenv
from collections import OrderedDict
from flask import current_app as app
from subprocess import Popen, check_output

load_dotenv("/etc/default/dclient")


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def get_installed(rpm):
    app.logger.info(f"running check_output(['rpm', '-q', {rpm}])")
    package = check_output(["rpm", "-q", rpm])
    z = re.match("not installed", package)
    if z:
        return False
    else:
        return True


def get_yum_transaction_id():
    app.logger.info("running check_output(['sudo', 'yum', 'history', 'list''])")
    history_list = check_output(["sudo", "yum", "history", "list"])
    history_list = history_list.splitlines()
    count = 0
    fl = 0
    for line in history_list:
        line = str(line, "utf-8")
        z = re.match("^-+$", line)
        if z:
            fl = count + 1
            count += 1
        else:
            count += 1
    first = history_list[fl]
    first = str(first, "utf-8")
    first = first.split("|")
    tid = first[0]
    tid = int(tid)
    return tid


def install_pkgs(packages):
    packages = " ".join(map(str, packages))
    app.logger.info("running os.system('sudo yum clean all')")
    os.system("sudo yum clean all")
    app.logger.info(f"running sudo yum --enablerepo=Production -y install {packages}")
    stat = os.system(f"sudo yum --enablerepo=Production -y install {packages}")
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    app.logger.info(f"running Popen(['sudo', 'systemctl', 'restart', {service}])")
    Popen(["sudo", "systemctl", "restart", service])


def update_env(key, value):
    """
    Set a key value pair in the environment file and export to the os
    :param: key string
    :param: value string
    :return: True or False
    """
    try:
        os.environ[key] = value
        env = LastUpdated()
        with open(Config.ENV_FILE) as f:
            for line in f:
                try:
                    (k, v) = line.split("=", 1)
                    env[k] = v
                except:
                    pass
        env[key] = value

        with open(Config.ENV_FILE, "w") as f:
            for k in env.keys():
                line = f"{k}={env[k]}"
                if "\n" in line:
                    f.write(line)
                else:
                    f.write(line + "\n")
        return True
    except Exception as e:
        app.logger.error(f"Update Environment Failed: {e}")
        return False


def set_state(state):
    """
    Set the dclient state in the environment and the deployment-api to the correct state.
    :param: state enum[NEW ACTIVE UPDATING ERROR DISABLED]
    :return: True or False
    """
    try:
        data = {"hostname": get_var("HOSTNAME"), "state": state}
        http = get_http()
        r = http.patch(
            f"{Config.DEPLOYMENT_API_URI}/server",
            json=data,
        )
        resp = r.json()
        app.logger.debug(f"Updated Proxy: {resp} {r.status_code}")
        update_env("STATE", state)
        os.environ["STATE"] = state
        return True
    except Exception as e:
        app.logger.error(f"SET STATE FAILED: {e}")
        return False


def register_dclient():
    """Register dclient and fetch token
    :return:
    """

    data = {
        "created_by": "dclient",
        "hostname": get_var("HOSTNAME"),
        "ip": get_var("IP"),
        "port": get_var("PORT"),
        "protocol": get_var("PROTOCOL"),
        "version": get_var("VERSION"),
        "state": "ACTIVE",
        "group": get_var("GROUP"),
        "environment": get_var("ENVIRONMENT"),
        "location": get_var("LOCATION"),
        "url": get_var("URL"),
        "deployment_proxy": get_var("DEPLOYMENT_PROXY"),
    }
    http = get_http()
    r = http.post(f"{Config.DEPLOYMENT_API_URI}/register", json=data)
    resp = r.json()
    app.logger.debug(f"REGISTER CLIENT: {resp}")
    if "server" in resp:
        update_env("SERVER_ID", resp["server"]["id"])
    if "token" in resp:
        update_env("TOKEN", resp["token"])
        set_state("ACTIVE")
        return True
    else:
        set_state("ERROR")
        return False
