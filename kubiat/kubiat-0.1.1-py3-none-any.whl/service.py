import logging
from flask import Flask

APP = Flask(__name__)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    APP.logger.handlers = gunicorn_logger.handlers
    APP.logger.setLevel(gunicorn_logger.level)
