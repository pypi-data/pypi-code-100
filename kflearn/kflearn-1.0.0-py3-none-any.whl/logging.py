#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 18, 2021
'''
import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler


class LoggerInfo:

    def __init__(self, name, log_path="/opt/logs/app", log_file_name="app.log"):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 配置输出日志格式
        # log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t%(process)d\t%(threadName)s\t%(message)s"
        log_format = "%(asctime)s\t%(levelname)s\t%(process)d\t%(thread)d\t%(module)s\t%(funcName)s\t%(message)s"
        self.Logger = logging.getLogger(name)
        self.Logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            fmt=log_format
        )
        if not self.Logger.handlers:
            handler = ConcurrentRotatingFileHandler(filename=os.path.join(log_path, log_file_name),
                                                    maxBytes=50 * 1024 * 1024, backupCount=10)
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            self.Logger.addHandler(handler)
