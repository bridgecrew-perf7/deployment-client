from dclient.config import Config

import os
import re
import logging
import requests
from collections import OrderedDict
from subprocess import Popen, check_output
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def set_state():
    """
    Set the dclient state to the correct state.
    Keep the state in sync with Deployment-api
    :return:
    """
    if not os.getenv("TOKEN"):
        register_dclient()
    else:
        update_env("STATE", "ACTIVE")
        headers = {"Authorization": Config.TOKEN}
        payload = {"hostname": Config.HOSTNAME, "state": "UPDATING"}
        http = get_http()
        http.patch(f"{Config.DEPLOYMENT_SERVER_URL}/server", headers=headers, json=payload)


def register_dclient():
    """
    Register dclient and fetch token
    :return:
    """
    data = {
        "created_by": "dclient",
        "hostname": Config.HOSTNAME,
        "ip": Config.IP,
        "state": "NEW",
        "group": Config.GROUP,
        "environment": Config.ENVIRONMENT,
        "location": Config.LOCATION,
        "url": Config.URL,
        "deployment_proxy": Config.DEPLOYMENT_PROXY
    }
    http = get_http()
    r = http.post("{}/register".format(Config.DEPLOYMENT_SERVER_URL), json=data)
    resp = r.json()
    if "token" in resp:
        update_env("TOKEN", resp["token"])
        update_env("STATE", "ACTIVE")


def get_http():
    retry_strategy = Retry(
        total=Config.RETRY,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


def get_logger():
    logger = logging.getLogger("dclient")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("/var/log/deployment/dclient.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


logger = get_logger()


class LastUpdated(OrderedDict):

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def get_installed(rpm):
    logger.info(f"running check_output(['rpm', '-q', {rpm}])")
    installed = check_output(["rpm", "-q", rpm])
    z = re.match("not installed", installed)
    if z:
        return False
    else:
        return True


def get_yum_transaction_id():
    logger.info("running check_output(['sudo', 'yum', 'history', 'list''])")
    history_list = check_output(["sudo", "yum", "history", "list"])
    history_list = history_list.splitlines()
    count = 0
    fl = 0
    for line in history_list:
        line = str(line, 'utf-8')
        z = re.match("^-+$", line)
        if z:
            fl = count + 1
            count += 1
        else:
            count += 1
    first = history_list[fl]
    first = str(first, 'utf-8')
    first = first.split("|")
    tid = first[0]
    tid = int(tid)
    return tid


def install_pkgs(packages):
    packages = ' '.join(map(str, packages))
    logger.info("running os.system('sudo yum clean all')")
    os.system("sudo yum clean all")
    logger.info(f"running sudo yum --enablerepo=Production -y install {packages}")
    stat = os.system(f"sudo yum --enablerepo=Production -y install {packages}")
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    logger.info(f"running Popen(['sudo', 'systemctl', 'restart', {service}])")
    Popen(["sudo", "systemctl", "restart", service])


def update_env(key, value):
    logger.info(f"Updating Environment: {key}={value}")
    env = LastUpdated()
    with open("/etc/default/dclient") as f:
        for line in f:
            (k, v) = line.split("=", 1)
            env[k] = v
    env[key] = value
    os.environ[key] = value

    with open("/etc/default/dclient", "w") as f:
        for k in env.keys():
            line = f"{k}={env[k]}"
            if "\n" in line:
                f.write(line)
            else:
                f.write(line+"\n")
