import os
from os.path import isfile


def kill_if_already_exist(app_name, pid_path):
    """is PID exists ? If right, try to kill it."""
    if not isfile(pid_path):
        with open(pid_path, 'w') as f:
            f.write(str(os.getpid()))
        return

    with open(pid_path, 'r') as f:
        pid = f.read()
    if pid == '':
        return
    try:
        os.kill(int(pid), 0)
    except OSError:
        return
    else:
        print(
            '** %s is already running\nOtherwise, delete %s' % (
                app_name, pid_path
            )
        )
        quit()


def remove(pid):
    """remove file with current process pid"""
    if isfile(pid):
        os.remove(pid)
