from dclient.util.logger import get_logger

import os
from dotenv import load_dotenv
from collections import OrderedDict

logger = get_logger()


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


environment_file = "/etc/default/dclient"
if os.getenv("ENV_FILE"):
    environment_file = os.getenv("ENV_FILE")
try:
    load_dotenv(environment_file)
except Exception as e:
    raise Exception(f"Unable to load environment {environment_file}: {e}")

config_file = "/etc/deployment/dclient.conf"
if os.getenv("CONFIG_FILE"):
    config_file = os.getenv("CONFIG_FILE")
config = LastUpdated()
try:
    with open(config_file) as cfg:
        for line in cfg:
            try:
                (k, v) = line.split("=", 1)
                config[k] = v
            except:
                pass
except Exception as e:
    raise Exception(f"Unable to load configuration {config_file}: {e}")


def get_var(var):
    if os.getenv(var):
        return os.getenv(var)
    else:
        if var in config:
            return config[var]
        else:
            return None


class Config(object):
    HOSTNAME = get_var("HOSTNAME")
    IP = get_var("IP")
    STATE = get_var("STATE")
    LOCATION = get_var("LOCATION")
    ENVIRONMENT = get_var("ENVIRONMENT")
    GROUP = get_var("GROUP")
    DEPLOYMENT_API_URI = get_var("DEPLOYMENT_API_URI")
    DEPLOYMENT_PROXY = get_var("DEPLOYMENT_PROXY")
    TOKEN = get_var("TOKEN")
    ENV_FILE = get_var("ENV_FILE")
    RETRY = get_var("RETRY")
    BACKOFF_FACTOR = get_var("BACKOFF_FACTOR")
    STATUS_FORCELIST = get_var("STATUS_FORCELIST")
    METHOD_WHITELIST = get_var("METHOD_WHITELIST")
    DEFAULT_TIMEOUT = get_var("DEFAULT_TIMEOUT")
