import os
import logging
import requests
from dotenv import load_dotenv
load_dotenv(".env")


def get_default(key):
    env = {}
    with open("/etc/default/dclient") as file:
        for line in file:
            (k, v) = line.split("=")
            env[k] = v
    os.environ[key] = env[key]
    return env[key]


def get_hostname():
    if os.getenv("HOSTNAME"):
        return os.getenv("HOSTNAME")
    else:
        return get_default("HOSTNAME")


def get_ip():
    if os.getenv("IP"):
        return os.getenv("IP")
    else:
        return get_default("IP")


def get_state():
    if os.getenv("STATE"):
        return os.getenv("STATE")
    else:
        return get_default("STATE")


def get_location():
    if os.getenv("LOCATION"):
        return os.getenv("LOCATION")
    else:
        return get_default("LOCATION")


def get_environment():
    if os.getenv("ENVIRONMENT"):
        return os.getenv("ENVIRONMENT")
    else:
        return get_default("ENVIRONMENT")


def get_group():
    if os.getenv("GROUP"):
        return os.getenv("GROUP")
    else:
        return get_default("GROUP")


def get_url():
    if os.getenv("URL"):
        return os.getenv("URL")
    else:
        hostname = get_hostname()
        url = f"http://{hostname}:8003/"
        return url


def get_deployment_server_url():
    if os.getenv("DEPLOYMENT_SERVER_URL"):
        return os.getenv("DEPLOYMENT_SERVER_URL")
    else:
        return "http://deploy-proxy.hp.provo1.endurancemb.com/api/1.0.0"


def get_deployment_proxy():
    if os.getenv("DEPLOYMENT_PROXY"):
        return os.getenv("DEPLOYMENT_PROXY")
    else:
        return "deploy-proxy.hp.provo1.endurancemb.com"


def get_token():
    if os.getenv("TOKEN"):
        return os.getenv("TOKEN")
    else:
        data = {
            "created_by": "dclient",
            "hostname": get_hostname(),
            "ip": get_ip(),
            "state": "NEW",
            "group": get_group(),
            "environment": get_environment(),
            "location": get_location(),
            "url": get_url(),
            "deployment_proxy": get_deployment_proxy()
        }
        r = requests.post(f"{get_deployment_server_url()}/register", json=data)
        resp = r.json()
        if "token" in resp["token"]:
            return resp["token"]
        else:
            return None


class Config(object):
    HOSTNAME = get_hostname()
    IP = get_ip()
    STATE = get_state()
    LOCATION = get_location()
    ENVIRONMENT = get_environment()
    GROUP = get_group()
    URL = get_url()
    DEPLOYMENT_SERVER_URL = get_deployment_server_url()
    DEPLOYMENT_PROXY = get_deployment_proxy()
    TOKEN = get_token()


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
