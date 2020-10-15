from dclient.util import update_env

import os
import logging
import requests
from dotenv import load_dotenv
load_dotenv("/etc/default/dclient")


def get_logger():
    logger = logging.getLogger("bhdapi")
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


def get_env(var):
    if var in os.environ:
        return os.getenv(var)
    else:
        default = {
            "HOSTNAME": "",
            "IP": "",
            "STATE": "NEW",
            "LOCATION": "PROVO",
            "ENVIRONMENT": "PRODUCTION",
            "GROUP": ""
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
        r = requests.post(f"{get_deployment_server_url()}/register", json=data)
        resp = r.json()
        logger.info(resp)
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

