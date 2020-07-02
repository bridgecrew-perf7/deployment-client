import falcon
from dclient.controllers.rollback import *


class Rollback(object):
    def on_post(self, req, resp):
        response = post_rollback(self, data=req.media)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]
