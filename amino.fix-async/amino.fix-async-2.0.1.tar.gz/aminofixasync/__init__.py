__title__ = 'Amino.fix-async'
__author__ = 'Minori'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2022 Minori'
__version__ = '2.0.0'

from .acm import ACM
from .client import Client
from .sub_client import SubClient
from .socket import Callbacks, SocketHandler
from .lib.util import device, exceptions, headers, helpers, objects
from requests import get
from json import loads

__newest__ = loads(get("https://pypi.org/pypi/amino.fix-async/json").text)["info"]["version"]

if __version__ != __newest__:
    print(f"New version of {__title__} available: {__newest__} (Using {__version__})")
    print(f"To update to the latest version, write to pip this command - pip install --upgrade amino.fix-async")
    print("Discord link - https://discord.gg/Bf3dpBRJHj")
