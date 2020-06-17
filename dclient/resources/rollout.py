import falcon
from controllers.rollout import *


class Rollout(object):
    def on_post(self, req, resp):
        self.session = req.context.db_session
        response = post_rollout(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]
