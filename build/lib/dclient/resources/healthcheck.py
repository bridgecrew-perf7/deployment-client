import falcon
from dclient.controllers.healthcheck import *


class HealthCheck(object):
    def on_post(self, req, resp):
        response = post_healthcheck(self, data=req.media)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

    def on_get(self, req, resp):
        response = get_healthcheck(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

