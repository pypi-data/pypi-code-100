import os

import toml
from rich import print

__version__ = "0.1.0"

__home__ = os.path.expanduser("~")
__cfg_path__ = os.path.join(__home__, ".pyfund.toml")

__data_path__ = os.path.join(__home__, "pyfund_datas")

try:
    __data_path__ = toml.load(__cfg_path__).get("data_path")
except FileNotFoundError:
    pass

def log_future(fur):
    if fur.exception():
        print(fur.result())


def to_per(i):
    return "{:.2%}".format(i)


def ffloat(f: float):
    return "{:6.03f}".format(f)


def log(fn):
    def do(*args):
        if constants.IS_DEBUG:
            print("[blue]debug[/blue]:", fn.__module__ + "." + fn.__name__)
        return fn(*args)

    return do
