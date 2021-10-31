"""Initialize and bring in modules."""
from .log import Log  # noqa
from .base import BaseLog  # noqa
from .config import log_config  # noqa

# Version 2 logging
from .log2 import config_log, SetLog  # noqa
