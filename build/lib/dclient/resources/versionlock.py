import falcon
from dclient.controllers.versionlock import *


class VersionLock(object):
    def on_post(self, req, resp):
        response = post_versionlock(self, data=req.media)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

    def on_get(self, req, resp):
        response = get_versionlock(self)
        resp.body = json.dumps(response["body"])
        resp.status = response["status"]

