import falcon
from controllers.healthcheck import *


class HealthCheck(object):
    def on_post(self, req, resp):
        self.session = req.context.db_session
        response = post_healthcheck(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

    def on_get(self, req, resp):
        self.session = req.context.db_session
        response = get_healthcheck(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

