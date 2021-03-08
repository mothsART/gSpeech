from os.path import dirname, isdir, join
from sys import modules


def is_debug_mode():
    if (
        isdir(join(dirname(modules['speech'].__file__), '..', '.git'))
    ):
        return True
    return False
