import os
import yum
import dbus
import requests
from flask import request

from dclient.config import Config


def install_pkgs(packages):
    packages = [x.encode("utf-8") for x in packages]
    yb = yum.YumBase()
    yb.setCacheDir()
    results = yb.pkgSack.returnNewestByNameArch(patterns=packages)
    for pkg in results:
        yb.install(pkg)
    yb.buildTransaction()
    yb.processTransaction()


def post_update():
    data = request.get_json()

    # Post state updating
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    requests.patch("{}/server".format(Config.DEPLOYMENT_SERVER_URL), headers=headers, json=payload, verify=False)

    for pkg in data["packages"]:
        os.system("yum versionlock add " + pkg)
    install_pkgs(data["packages"])

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
    manager = dbus.Interface(systemd1, "org.freedesktop.systemd1.Manager")
    manager.RestartUnit("dclient.service", "fail")
