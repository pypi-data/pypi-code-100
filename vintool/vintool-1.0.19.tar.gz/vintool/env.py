#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import configparser

__environments = dict()


def is_json(text):
    try:
        float(text)
        return False
    except ValueError as e:
        try:
            json.loads(text)
            return True
        except ValueError as e:
            return False


def get(key, default=None):
    """
    支持二级配置 . 号分割
    """
    if key.find('.') < 0:
        if key in __environments:
            return __environments[key]
        else:
            return default
    else:
        if key in __environments: return __environments[key]
        keys = key.split('.')
        if keys[0] in __environments and '.'.join(keys[1:]) in __environments[keys[0]]:
            return __environments[keys[0]]['.'.join(keys[1:])]
        else:
            return default


def init(env=None):
    global __environments
    # 读取环境变量
    env_dist = os.environ
    for key in env_dist:
        if is_json(env_dist[key]):
            __environments[key] = json.loads(env_dist[key])
            pass
        else:
            if key.find('.') < 0:
                __environments[key] = env_dist[key]
            else:
                keys = key.split('.')
                if keys[0] not in __environments:
                    __environments[keys[0]] = {'.'.join(keys[1:]): env_dist[key]}
                else:
                    val = __environments[keys[0]]
                    val['.'.join(keys[1:])] = env_dist[key]
                    __environments[keys[0]] = val
    # 读取本地文件配置(本地配置会覆盖环境变量)
    if env:
        if not os.path.exists(env): raise EnvException("env file not found: %s" % env)
        cfs = configparser.ConfigParser()
        cfs.read(env)
        for section in cfs.sections():
            __environments[section] = {}
            for option in cfs[section]:
                __environments[section][option] = cfs.get(section, option)


class EnvException(Exception):
    pass
