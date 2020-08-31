def get_healthcheck():
    response = {
        "status": "success",
        "message": "system is healthy"
    }
    return response, 200
