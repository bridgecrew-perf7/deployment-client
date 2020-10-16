import os
import re
import socket
import logging
import requests
from dotenv import load_dotenv
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from subprocess import Popen, check_output
from requests.packages.urllib3.util.retry import Retry

load_dotenv("/etc/default/dclient")


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
    """
    Update environment variables and store environment file
    :param key:
    :param value:
    :return:
    """
    logger.info(f"Updating Environment: {key}={value}")
    env = LastUpdated()
    with open(Config.ENV_FILE) as f:
        for line in f:
            (k, v) = line.split("=", 1)
            env[k] = v
    env[key] = value
    os.environ[key] = value

    with open(Config.ENV_FILE, "w") as f:
        for k in env.keys():
            line = f"{k}={env[k]}"
            if "\n" in line:
                f.write(line)
            else:
                f.write(line+"\n")


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
    logger.info(f"REGISTER CLIENT: {resp}")
    if "token" in resp:
        update_env("TOKEN", resp["token"])
        update_env("STATE", "ACTIVE")


def get_env(var):
    if var in os.environ:
        return os.getenv(var)
    else:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        default = {
            "HOSTNAME": hostname,
            "IP": ip,
            "STATE": "NEW",
            "LOCATION": "PROVO",
            "ENVIRONMENT": "PRODUCTION",
            "GROUP": "",
            "RETRY": 10,
            "ENV_FILE": "/etc/default/dclient"
        }
        return default[var]


def get_url():
    if os.getenv("URL"):
        return os.getenv("URL")
    else:
        if os.getenv("HOSTNAME"):
            url = f"http://{os.getenv('HOSTNAME')}:8003/"
            update_env("URL", url)
            return url
        else:
            return None


def get_deployment_server_url():
    if os.getenv("DEPLOYMENT_SERVER_URL"):
        return os.getenv("DEPLOYMENT_SERVER_URL")
    else:
        update_env("DEPLOYMENT_SERVER_URL", "http://deploy-proxy.hp.provo1.endurancemb.com:8002/api/1.0.0")
        return "http://deploy-proxy.hp.provo1.endurancemb.com:8002/api/1.0.0"


def get_deployment_proxy():
    if os.getenv("DEPLOYMENT_PROXY"):
        return os.getenv("DEPLOYMENT_PROXY")
    else:
        update_env("DEPLOYMENT_PROXY", "deploy-proxy.hp.provo1.endurancemb.com")
        return "deploy-proxy.hp.provo1.endurancemb.com"


def get_token():
    if os.getenv("TOKEN"):
        return os.getenv("TOKEN")
    else:
        data = {
            "created_by": "dclient",
            "hostname": get_env("HOSTNAME"),
            "ip": get_env("IP"),
            "state": "NEW",
            "group": get_env("GROUP"),
            "environment": get_env("ENVIRONMENT"),
            "location": get_env("LOCATION"),
            "url": get_url(),
            "deployment_proxy": get_deployment_proxy()
        }
        http = get_http()
        r = http.post(f"{get_deployment_server_url()}/register", json=data)
        resp = r.json()
        if "token" in resp:
            update_env("TOKEN", resp["token"])
            return resp["token"]
        else:
            return None


class Config(object):
    HOSTNAME = get_env("HOSTNAME")
    IP = get_env("IP")
    STATE = get_env("STATE")
    LOCATION = get_env("LOCATION")
    ENVIRONMENT = get_env("ENVIRONMENT")
    GROUP = get_env("GROUP")
    URL = get_url()
    DEPLOYMENT_SERVER_URL = get_deployment_server_url()
    DEPLOYMENT_PROXY = get_deployment_proxy()
    TOKEN = get_token()
    RETRY = get_env("RETRY")
    ENV_FILE = get_env("ENV_FILE")