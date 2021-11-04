# -*- coding: UTF-8 -*-
# @Time     : 2020/7/10 10:22
# @Author   : Jackie
# @File     : handlerRedis.py

import redis
from .read_config import apollo_reader
from .logger import logger


class HandlerRedis:
    def __init__(self):
        self.config = {
            'host': apollo_reader.get_value('redis.host'),
            'port': int(apollo_reader.get_value('redis.port')),
            'password': apollo_reader.get_value('redis.password'),
            'db': apollo_reader.get_value('redis.db'),
            'decode_responses': True,
        }

        self.default_ex = 3600 * 24
        self.pool = redis.ConnectionPool(**self.config)
        self.rds = redis.Redis(connection_pool=self.pool)
        self.pipe = self.rds.pipeline()
        logger.info('[%s] connected.' % self)

    def __str__(self):
        return 'Redis[{host}:{port}], db[{db}]'.format(**self.config)

    def set_ex(self, key, value, ex=3600*24):
        if ex == self.default_ex:
            ex = self.rds.ttl(key)
        if ex > 0:
            self.rds.setex(key, ex, value)
        else:
            self.rds.setex(key, self.default_ex, value)

    def lpush(self, key, data):
        self.rds.lpush(key, data)

    def llen(self, key):
        self.rds.llen(key)


def get_rds_handler():
    return HandlerRedis()
