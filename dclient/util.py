import os
import re
from collections import OrderedDict
from subprocess import Popen, check_call, check_output


class LastUpdated(OrderedDict):

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def get_yum_transaction_id():
    history_list = check_output(["yum", "history", "list"])
    history_list = history_list.splitlines()
    count = 0
    fl = 0
    for line in history_list:
        line = str(line, 'utf-8')
        z = re.match("^-+$", line)
        if z:
            fl = count + 1
            count += 1
        else:
            count += 1
    first = history_list[fl]
    first = str(first, 'utf-8')
    first = first.split("|")
    tid = first[0]
    tid = int(tid)
    return tid


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    check_call("sudo yum clean all")
    stat = check_call("sudo yum -y --enablerepo=Production install {}".format(packages))
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    Popen(["systemctl", "restart", service])


def update_env(key, value):
    env = LastUpdated()
    with open(".env") as f:
        for line in f:
            (k, v) = line.split("=")
            env[k] = v
    env[key] = value
    os.environ[key] = value

    with open(".env", "w") as f:
        for k in env.keys():
            line = f"{k}={env[k]}\n"
            f.write(line)
