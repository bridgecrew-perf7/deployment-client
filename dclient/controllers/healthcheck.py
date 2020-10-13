from dclient.config import Config


def get_healthcheck():
    response = {
        "hostname": Config.HOSTNAME,
        "status": "SUCCESS",
        "message": "system is healthy"
    }
    return response, 200
