import os
import logging
from dotenv import load_dotenv
load_dotenv("/etc/default/dclient")


class Config:
    HOSTNAME = os.getenv("HOSTNAME")
    IP = os.getenv("IP")
    STATE = os.getenv("STATE")
    LOCATION = os.getenv("LOCATION")
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    GROUP = os.getenv("GROUP")
    URL = os.getenv("URL")
    DEPLOYMENT_SERVER_URL = os.getenv("DEPLOYMENT_SERVER_URL")
    DEPLOYMENT_PROXY = os.getenv("DEPLOYMENT_PROXY")
    TOKEN = os.getenv("TOKEN")


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
