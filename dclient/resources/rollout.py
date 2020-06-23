import falcon
from dclient.controllers.rollout import *


class Rollout(object):
    def on_post(self, req, resp):
        response = post_rollout(self, data=req.media)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]
