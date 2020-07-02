import os
import logging
import logging.handlers
from dotenv import load_dotenv


class Config:
    if not os.path.exists("/var/log/dclient"):
        os.makedirs("/var/log/dclient")
        with open("/var/log/dclient/access.log", "w") as file:
            pass
        with open("/var/log/dclient/error.log", "w") as file:
            pass

    if os.path.exists("/etc/default/dclient"):
        load_dotenv("/etc/default/dclient")
        TOKEN = os.getenv("TOKEN")
    else:
        with open("/etc/default/dclient", "w") as file:
            pass

    if TOKEN:
        TOKEN = os.getenv("TOKEN")
    access_log = logging.getLogger(__name__)
    access_log.setLevel(logging.INFO)
    access_handler = logging.FileHandler("/var/log/dclient/access.log")
    access_formatter = logging.Formatter("%(module)s.%(funcName)s: %(message)s")
    access_handler.setFormatter(access_formatter)
    access_log.addHandler(access_handler)
    error_log = logging.getLogger(__name__)
    error_log.setLevel(logging.ERROR)
    error_handler = logging.FileHandler("/var/log/dclient/error.log")
    error_formatter = logging.Formatter("%(module)s.%(funcName)s: %(message)s")
    error_handler.setFormatter(error_formatter)
    error_log.addHandler(error_handler)
