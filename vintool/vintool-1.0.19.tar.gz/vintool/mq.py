#! /usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
from .rabbit_mq import Rabbitmq, BaseMq, Producer, Consumer

__instance = {}


def __get_instance(**kwargs):
    config, driver = BaseMq.get_config(**kwargs)
    config_key = hashlib.md5(json.dumps(config).encode("utf8")).hexdigest()
    if config_key not in __instance:
        __instance[config_key] = Rabbitmq(config)
    return __instance[config_key]


def publish(message, *args, **kwargs):
    producer = Producer(__get_instance(**kwargs))
    res = producer.publish(message, *args, **kwargs)
    __channel1 = None
    return res


def consume(callback, queue=None, *args, **kwargs):
    consumer = Consumer(__get_instance(**kwargs))
    res = consumer.consume(callback, queue, *args, **kwargs)
    return res
