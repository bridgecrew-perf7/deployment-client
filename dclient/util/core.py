from dclient.util.config import Config, get_var
from dclient.util.http_helper import get_http
<<<<<<< HEAD

=======
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
import os
import re
from dotenv import load_dotenv
from collections import OrderedDict
from flask import current_app as app
from subprocess import Popen, check_output
from flask import current_app as app

load_dotenv("/etc/default/dclient")

<<<<<<< HEAD
=======

>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac

class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


<<<<<<< HEAD
def get_installed(rpm):
    app.logger.info(f"running check_output(['rpm', '-q', {rpm}])")
    package = check_output(["rpm", "-q", rpm])
    z = re.match("not installed", package)
    if z:
        return False
    else:
=======
def not_installed(rpm):
    app.logger.debug(f"running rpm -q {rpm}")
    stat = os.system(f"rpm -q {rpm}")
    if stat == 1:
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        return True
    else:
        return False


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
<<<<<<< HEAD
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
=======
        env = LastUpdated()
        with open("/etc/default/dclient") as f:
            for line in f:
                (k, v) = line.split("=", 1)
                env[k] = v
        env[key] = value
        os.environ[key] = value
    except:
        raise Exception("Unable to process dclient environment file.")

    try:
        with open("/etc/default/dclient", "w") as f:
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
            for k in env.keys():
                line = f"{k}={env[k]}"
                if "\n" in line:
                    f.write(line)
                else:
                    f.write(line + "\n")
<<<<<<< HEAD
        return True
    except Exception as e:
        app.logger.error(f"Update Environment Failed: {e}")
        return False
=======
    except:
        raise Exception("Unable to update dclient environment file.")
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac


def set_state(state):
    """
    Set the dclient state in the environment and the deployment-api to the correct state.
    :param: state enum[NEW ACTIVE UPDATING ERROR DISABLED]
    :return: True or False
    """
<<<<<<< HEAD
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
=======
    data = {
        "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "port": Config.DEPLOYMENT_CLIENT_PORT,
        "version": Config.DEPLOYMENT_CLIENT_VERSION,
        "state": state,
    }
    http = get_http()
    r = http.patch(f"{Config.DEPLOYMENT_API_URI}/server", json=data)
    if r.status_code == 201:
        app.logger.debug(f"Successfully Updated State: {state}")
        return True
    else:
        app.logger.error(f"Failed to set state: {state}")
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        return False


def register_dclient():
    """Register dclient and fetch token
    :return:
    """

    data = {
        "created_by": "dclient",
<<<<<<< HEAD
        "hostname": get_var("HOSTNAME"),
        "ip": get_var("IP"),
        "port": get_var("PORT"),
        "protocol": get_var("PROTOCOL"),
        "version": get_var("VERSION"),
=======
        "protocol": Config.DEPLOYMENT_CLIENT_PROTOCOL,
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "port": Config.DEPLOYMENT_CLIENT_PORT,
        "version": Config.DEPLOYMENT_CLIENT_VERSION,
        "ip": Config.DEPLOYMENT_CLIENT_IP,
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
        "state": "ACTIVE",
        "group": Config.GROUP,
        "environment": Config.ENVIRONMENT,
        "location": Config.LOCATION,
        "deployment_proxy": Config.DEPLOYMENT_PROXY_HOSTNAME,
    }
    http = get_http()
    r = http.post(f"{Config.DEPLOYMENT_API_URI}/register", json=data)
    resp = r.json()
    app.logger.debug(f"REGISTER CLIENT: {resp}")
<<<<<<< HEAD
    if "server" in resp:
        update_env("SERVER_ID", resp["server"]["id"])
=======
>>>>>>> 8163e4905e6bab0d330c90f6ae74b6191c9d55ac
    if "token" in resp:
        update_env("TOKEN", resp["token"])
        set_state("ACTIVE")
        return True
    else:
        set_state("ERROR")
        return False
