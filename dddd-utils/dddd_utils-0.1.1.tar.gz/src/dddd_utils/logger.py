# -*- coding: utf-8 -*-
"""
log
"""
__all__ = [
    'get_logger'
]

import logging


def get_logger(logger_name=None, log_level=logging.DEBUG, log_file_path=None):
    """获取logger"""
    format = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=format, datefmt=datefmt)

    # 控制台输出
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 日志文件
    if log_file_path is not None:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level=log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
