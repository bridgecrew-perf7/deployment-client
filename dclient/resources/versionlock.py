import falcon
from controllers.versionlock import *


class VersionLock(object):
    def on_post(self, req, resp):
        self.session = req.context.db_session
        response = post_versionlock(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

    def on_get(self, req, resp):
        self.session = req.context.db_session
        response = get_versionlock(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

