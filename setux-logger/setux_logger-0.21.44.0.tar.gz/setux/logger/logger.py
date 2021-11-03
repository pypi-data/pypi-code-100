from logging import getLogger
from logging.config import dictConfig

from setux.core.logger import Logger, Deploy
from .config import config


dictConfig(config)


logger = Logger(getLogger('Setux'))

debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception


deploy = Deploy(getLogger('Deploy'), logger)

green = deploy.green
yellow = deploy.yellow
red = deploy.red
