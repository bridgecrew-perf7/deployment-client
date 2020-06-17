import falcon
from controllers.rollback import *


class Rollback(object):
    def on_post(self, req, resp):
        self.session = req.context.db_session
        response = post_rollback(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]
