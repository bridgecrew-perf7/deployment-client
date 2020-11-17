from dclient.util.config import Config

from flask import current_app as app


def get_healthcheck():
    response = {
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "status": "SUCCESS",
        "message": "system is healthy",
    }
    app.logger.debug(response)
    return response, 200
