from .lib import objects, exceptions
from .threads import *
from .client import Client

from json import loads
from requests import get

try:
    __version__ = '1.0.0.2'
    __newest__ = loads(get("https://pypi.python.org/pypi/capture.py/json").text)["info"]["version"]
    if __version__ != __newest__:
        print(f"\033[1;33mCaptureS New Version!: {__newest__} (Your Using {__version__})\033[1;0m")
finally:
    pass

# This library officially Created By SirLez!
