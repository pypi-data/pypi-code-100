from .version import get_version

VERSION = (0, 0, 1, "final", 0)
__version__ = get_version(VERSION)

default_app_config = "slunic.apps.SlunicConfig"
