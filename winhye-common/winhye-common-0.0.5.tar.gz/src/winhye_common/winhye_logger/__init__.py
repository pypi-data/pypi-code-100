import datetime
import os
from logging import *
import logging.config

from .filter import HostAddressFilter, RequestAddressFilter, ConcurrentIdFilter
from .weather import weather_report

__all__ = ["logging"]

# new logging level REPORT
REPORT = 100
logging.addLevelName(REPORT, "REPORT")
log_dir = "/data/log/flask/"


def logger_report(self, msg: str, weather: bool = False, *args, **kwargs):
    """
    Report level for logger, support report weather

    :param msg: dict, report content
    :param weather: bool, report to whether, default is False
    """
    if self.isEnabledFor(REPORT):
        self._log(REPORT, msg, args, **kwargs)
    if weather is True:
        weather_report()


logging.Logger.report = logger_report

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "winhye": {
            "format": "[%(asctime)s] <host=%(hostname)s source=%(source_ip)s> %(filename)s line:%(lineno)d <process=%(process)d concurrent=%(concurrent_id)d> [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "filters": {
        "hostname": {
            "()": HostAddressFilter
        },
        "source_ip": {
            "()": RequestAddressFilter
        },
        "concurrent_id": {
            "()": ConcurrentIdFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "winhye",
            "filters": ["hostname", "source_ip", "concurrent_id"]
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(log_dir, "log.log"),
            "formatter": "winhye",
            "filters": ["hostname", "source_ip", "concurrent_id"],
            "when": "H",
            "interval": 1,
            "backupCount": 168,
            "atTime": datetime.datetime.now(),
            "delay": False
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",  # logger日志输出级别
            "handlers": ["console", "file"],
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["file"],
            "propagate": True,
            "qualname": "gunicorn.error"
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["file"],
            "propagate": True,
            "qualname": "gunicorn.access"
        },
    }
}

# 新建log目录
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.config.dictConfig(logging_config)
