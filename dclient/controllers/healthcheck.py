from dclient.util.config import Config
from flask import current_app as app


def get_healthcheck():
    app.logger.info("HealthCheck!")
    response = {
        "hostname": Config.DEPLOYMENT_CLIENT_HOSTNAME,
        "status": "SUCCESS",
        "message": "system is healthy",
    }
    return response, 200
