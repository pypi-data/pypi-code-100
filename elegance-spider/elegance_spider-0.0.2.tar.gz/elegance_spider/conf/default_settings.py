import logging

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s[line:%(lineno)d] \
                  %(levelname)s: %(message)s'
DEFAULT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_FILENAME = 'log.log'

SPIDERS = []
PIPLINES =[]
SPIDER_MIDDLEWARES = []
DOWNLOADER_MIDDLEWARES = []