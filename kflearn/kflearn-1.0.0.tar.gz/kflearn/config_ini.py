#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 18, 2021
'''

import os
import configparser
from configparser import ConfigParser
import logging

"""
配置读取类
用于读取Conf路径下配置文件
文件命名格式如：app-sit.ini ，sit为环境类型
"""


class KFLConf(object):

    def __init__(self, conf_file='train.ini'):
        self.__conf = {}
        self.set_conf_file(conf_file)

    def set_conf_file(self, conf_file='train.ini'):
        cp = ConfigParser()
        cp.read(conf_file, encoding='utf8')

        # 1-先从配置文件-->conf_dict
        # [required]
        self.__conf['train_name'] = cp.get('required', 'train_name')  # 训练名称
        self.__conf['train_version'] = cp.get('required', 'train_version')
        self.__conf['train_algo_type'] = cp.get('required', 'train_algo_type')
        # [default]
        self.__conf['model_dir'] = cp.get('default', 'model_dir')
        self.__conf['train_dir'] = cp.get('default', 'train_dir')
        self.__conf['valid_dir'] = cp.get('default', 'valid_dir')
        self.__conf['test_dir'] = cp.get('default', 'test_dir')
        self.__conf['metrics_dir'] = cp.get('default', 'metrics_dir')

        logging.info('load config [%s] file success.' % conf_file)
        return self

    def set(self, conf_key=None, conf_value=None, conf_dict: dict = None):
        if conf_key is not None and conf_value is not None:
            self.__conf[conf_key] = conf_value
        elif conf_dict is not None:
            self.__conf.update(conf_dict)
        else:
            raise Exception('配置输入参数异常')
        return self

    def get(self, conf_key):
        return self.__conf[conf_key]

    def build(self):
        # 2-再从conf_dict-->固定变量
        self.train_name = self.__conf['train_name']
        self.train_version = self.__conf['train_version']
        self.train_algo_type = self.__conf['train_algo_type']

        self.model_dir = self.__conf['model_dir']
        self.train_dir = self.__conf['train_dir']
        self.valid_dir = self.__conf['valid_dir']
        self.test_dir = self.__conf['test_dir']
        self.metrics_dir = self.__conf['metrics_dir']

        logging.info('Train conf_dict=' + str(self.__conf))
        return self


class Config(object):
    def __init__(self, service_name=os.getenv("MODELX_SERVICE_NAME"),
                 env_type=os.getenv("ENV_TYPE"),
                 absolute_path="/opt/files"):
        self.service_name = service_name
        self.env_type = env_type
        self.work_path = absolute_path
        self._conf_path = '{}/{}/conf/app-{}.ini'.format(self.work_path, self.service_name, self.env_type)
        self._conf = configparser.ConfigParser()
        self._conf.read(self._conf_path)

    """
    return redis config attr 
    init Sentinel class, shard_name
    redis example:
        # 获取主节点，写入
        master = sentinel.master_for(shard_name, socket_timeout=0.5)
        # 获取从节点，读取
        slave = sentinel.slave_for(shard_name, socket_timeout=0.5)
        master.set('hht', input_data)
    """

    def get_redis_properties(self, attr_tag="redis"):
        from redis.sentinel import Sentinel
        sentinel1 = self._conf.get(attr_tag, "redis.sentinel1")
        sentinel2 = self._conf.get(attr_tag, "redis.sentinel2")
        sentinel3 = self._conf.get(attr_tag, "redis.sentinel3")
        port = self._conf.get(attr_tag, "redis.port")
        shard_name = self._conf.get(attr_tag, "redis.shardName")
        sentinel = Sentinel([(sentinel1, port), (sentinel2, port), (sentinel3, port)], socket_timeout=0.5)
        return sentinel, shard_name

    """
    return kafka config attr
    ---(1) 
    kafka consumer example：
        from kafka import KafkaConsumer
        topic,groupid,broker,zk = config.get_kafka_properties("kafka")
        consumer = KafkaConsumer(topic, group_id=groupid, bootstrap_servers=broker.split(","))
        for msg in consumer:
            recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            print(recv)
    ---
    ---(2) 
    kafka producer example:
        import json
        from kafka import KafkaProducer
        from kafka.errors import KafkaError
        producer = KafkaProducer(
            bootstrap_servers=broker.split(","),
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
        future = producer.send(topic, {
            "name": "xx",
            "age": 10,
            "friends": [
                "ritoyan",
                "luluyrt"
            ]
        })
    ---
    """

    def get_kafka_properties(self, attr_tag="kafka"):
        topic = self._conf.get(attr_tag, "kafka.topic")
        groupid = self._conf.get(attr_tag, "kafka.groupid")
        broker = self._conf.get(attr_tag, "kafka.broker")
        zookeeper = self._conf.get(attr_tag, "kafka.zookeeper")
        return topic, groupid, broker, zookeeper

    """
    return config
    """

    def get_properties(self):
        return self._conf


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    conf = KFLConf(conf_file='../kfl_core/config.yaml').set_conf_file(conf_file='../kfl_core/config.yaml') \
        .set('train_name', 'name00001') \
        .set('train_version', 'v1.0') \
        .set('auth', 'horn') \
        .build()

    # print(conf._KFLConf__conf)
