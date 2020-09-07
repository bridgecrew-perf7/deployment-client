import re
import dbus
from subprocess import check_output, check_call

from dclient.config import Config


def get_yum_transaction_id():
    history_list = sudo_cmd("yum history list", verbose=True)
    history_list = history_list.splitlines()
    count = 0
    fl = 0
    for line in history_list:
        z = re.match("^-+$", line)
        if z:
            fl = count + 1
            count += 1
        else:
            count += 1
    fl = history_list[fl].split("|")
    tid = fl[0]
    return tid


def sudo_cmd(cmd, verbose=None):
    sudo = Config.PASSWORD
    if verbose:
        return check_output("echo {} | sudo -S {}".format(sudo, cmd), bufsize=-1, shell=True)
    else:
        return check_call("echo {} | sudo -S {}".format(sudo, cmd), bufsize=-1, shell=True)


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    stat = sudo_cmd("yum -y install {}".format(packages), verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
    manager = dbus.Interface(systemd1, "org.freedesktop.systemd1.Manager")
    manager.RestartUnit(service, "fail")
