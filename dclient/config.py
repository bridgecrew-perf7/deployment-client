import os
from dotenv import load_dotenv
load_dotenv("/etc/default/dclient")


class Config:
    if "PUBLIC_IP" in os.environ:
        ip = os.getenv("PUBLIC_IP")
    else:
        ip = os.getenv("IP")
    HOSTNAME = os.getenv("HOSTNAME")
    IP = ip
    STATE = os.getenv("STATE")
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    GROUP = os.getenv("GROUP")
    LOCATION = os.getenv("LOCATION")
    TOKEN = os.getenv("TOKEN")
    DEPLOYMENT_SERVER_URL = os.getenv("DEPLOYMENT_SERVER_URL")
    DEPLOYMENT_PROXY = os.getenv("DEPLOYMENT_PROXY")
