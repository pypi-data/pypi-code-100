from os import getenv

__version__ = "0.0.4"
__name__ = "ppt-control"

CONFIG_DIR = getenv("APPDATA") + "\\" + __name__
CONFIG_FILE = __name__ + ".ini"
CONFIG_PATH = CONFIG_DIR + "\\" + CONFIG_FILE

LOG_DIR = getenv("APPDATA") + "\\" + __name__
LOG_FILE = __name__ + ".log"
LOG_PATH = LOG_DIR + "\\" + LOG_FILE
