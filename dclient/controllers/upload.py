import os
import json
from flask import request

from dclient.config import Config


def post_upload(file, data):
    """
    Recieve a file upload for dclient
    Write file to tmp
    Move file to permanent location and set permissions
    Example:
    {"name":"override.pm","location":"/var/hp/common/lib/config/","user":"root","group":"root","permissions":"0644"}
    :param self:
    :param file:
    :param data:
    :return:
    """
    pass
