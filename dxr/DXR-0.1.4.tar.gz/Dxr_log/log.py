# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
from logging import handlers

isPrintDebug = False
isPrintError = True
isPrintInfo = True


def setLogPrint(info=True, error=True, debug=False):
    global isPrintDebug, isPrintError, isPrintInfo
    isPrintInfo = info
    isPrintError = error
    isPrintDebug = debug


class Logger(object):
    #  日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s line %(lineno)s %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)  # 设置文件里写入的格式
        # self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if not os.path.exists(os.environ['HOME'] + '/log/'):  # 判断是否存在文件夹如果不存在则创建为文件夹
    try:
        os.makedirs(os.environ['HOME'] + '/log/')  # makedirs 创建文件时如果路径不存在会创建这个路径
    except Exception as ex:
        print(ex)
        pass

all_log = Logger(os.environ['HOME'] + '/log/all.log', level='info')
err_log = Logger(os.environ['HOME'] + '/log/error.log', level='error')
debug_log = Logger(os.environ['HOME'] + '/log/debug.log', level='debug')


def print_info(*args):
    global isPrintInfo
    try:
        all_log.logger.info(*args)
        if isPrintInfo:
            print(*args)
    except Exception as ex:
        print(ex)


def print_debug(*args):
    global isPrintDebug
    try:
        debug_log.logger.debug(*args)
        if isPrintDebug:
            print(*args)
    except Exception as ex:
        print(ex)


def print_error(*args):
    global isPrintError
    try:
        if isPrintError:
            print(*args)
        all_log.logger.debug(*args)
        err_log.logger.error(*args)
    except Exception as ex:
        print(ex)
