from dclient.util.config import Config
from dclient.util.logger import get_logger

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = get_logger()


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = int(Config.DEFAULT_TIMEOUT)
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_http():
    retry_strategy = Retry(
        total=int(Config.RETRY),
        backoff_factor=int(Config.BACKOFF_FACTOR),
        status_forcelist=list(Config.STATUS_FORCELIST),
        method_whitelist=list(Config.METHOD_WHITELIST)
    )
    http = requests.Session()
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retry_strategy))
    http.mount("http://", TimeoutHTTPAdapter(max_retries=retry_strategy))
    return http

