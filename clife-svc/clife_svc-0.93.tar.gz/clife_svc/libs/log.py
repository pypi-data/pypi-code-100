#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import os
from loguru import logger as klogger

LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                       'logs')  # 项目根目录/logs


def init_conf_log(log_path: str):
    '''
    初始化disconf日志模块
    :param log_path: 日志输出路径
    :return:
    '''
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    klogger.add(os.path.join(log_path, 'disconf.log'), filter='clife_svc.disconf')


def init_svc_log(log_path: str, log_level='INFO'):
    '''
    初始化服务日志模块
    :param log_path: 日志输出路径
    :param log_level: 日志级别，从低到高依次为 TRACE|DEBUG|INFO|SUCCESS|WARNING|ERROR|CRITICAL
    :return:
    '''
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    klogger.add(
        os.path.join(log_path, '{time:YYYY-MM-DD}.log'),
        # format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
        level=log_level,
        enqueue=True,
        rotation='500 MB',
        retention='7 days',
        encoding='utf-8',
        # serialize=True
    )


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
