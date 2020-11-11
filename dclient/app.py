#!/usr/bin/python3
from dclient.util.config import Config
from dclient.controllers.update import post_update
from dclient.controllers.rollout import post_rollout
from dclient.controllers.rollback import post_rollback
from dclient.util.core import set_state, register_dclient
from dclient.controllers.healthcheck import get_healthcheck
from dclient.controllers.versionlock import post_versionlock, get_versionlock

from flask import Flask, request

import logging.handlers

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

rotating_log_handeler = logging.handlers.RotatingFileHandler(Config.LOG_FILE, maxBytes=int(Config.LOG_MAX_BYTES),
                                                             backupCount=int(Config.LOG_BACKUP_COUNT))
rotating_log_handeler.setFormatter(formatter)
rotating_log_handeler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(rotating_log_handeler)


def create_app():
    """
    Create the dclient app
    :return: app
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        if not Config.TOKEN:
            register_dclient()
        else:
            set_state("ACTIVE")

        @app.route("/", methods=["GET"])
        def healthcheck():
            if request.method == "GET":
                return get_healthcheck()

        @app.route("/update", methods=["POST"])
        def update():
            if request.method == "POST":
                return post_update()

        @app.route("/rollout", methods=["POST"])
        def rollout():
            if request.method == "POST":
                return post_rollout()

        @app.route("/rollback", methods=["POST"])
        def rollback():
            if request.method == "POST":
                return post_rollback()

        @app.route("/versionlock", methods=["GET", "POST"])
        def versionlock():
            if request.method == "POST":
                return post_versionlock()
            elif request.method == "GET":
                return get_versionlock()

    return app
