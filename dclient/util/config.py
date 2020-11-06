import os
from dotenv import load_dotenv
from collections import OrderedDict


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


if os.getenv("ENV_FILE"):
    load_dotenv(os.getenv("ENV_FILE"))
elif os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("/etc/default/dclient"):
    load_dotenv("/etc/default/dclient")
else:
    raise Exception("No Environment File Found!")


def get_config():
    if os.getenv("CONFIG_FILE"):
        config_file = os.getenv("CONFIG_FILE")
    else:
        config_file = "/etc/deployment/dclient.conf"

    if os.path.exists(config_file):
        config = LastUpdated()
        with open(config_file) as cfg:
            for line in cfg:
                try:
                    (k, v) = line.split("=", 1)
                    config[k] = v
                except:
                    pass
        return config
    else:
        return None


def get_var(var):
    config = get_config()
    if os.getenv(var):
        return os.getenv(var)
    else:
        if config:
            if var in config:
                return config[var]
            else:
                return None
        else:
            return None


class Config(object):
    HOSTNAME = get_var("HOSTNAME")
    PORT = get_var("PORT")
    API_VERSION = get_var("API_VERSION")
    IP = get_var("IP")
    STATE = get_var("STATE")
    LOCATION = get_var("LOCATION")
    ENVIRONMENT = get_var("ENVIRONMENT")
    GROUP = get_var("GROUP")
    DEPLOYMENT_PROXY = get_var("DEPLOYMENT_PROXY")
    PROXY_PORT = get_var("PROXY_PORT")
    DEPLOYMENT_API_URI = (
        "http://" + DEPLOYMENT_PROXY + ":" + PROXY_PORT + "/api/" + API_VERSION
    )
    TOKEN = get_var("TOKEN")
    ENV_FILE = get_var("ENV_FILE")
    RETRY = get_var("RETRY")
    BACKOFF_FACTOR = get_var("BACKOFF_FACTOR")
    STATUS_FORCELIST = get_var("STATUS_FORCELIST")
    METHOD_WHITELIST = get_var("METHOD_WHITELIST")
    DEFAULT_TIMEOUT = get_var("DEFAULT_TIMEOUT")
    LOG_FILE = get_var("LOG_FILE")
    LOG_MAX_BYTES = get_var("LOG_MAX_BYTES")
    LOG_BACKUP_COUNT = get_var("LOG_BACKUP_COUNT")
