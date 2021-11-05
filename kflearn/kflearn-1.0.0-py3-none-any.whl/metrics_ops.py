#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 21, 2021
'''
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import *
import json
from kflearn.config_ops import KFLConf
from kflearn.constant_utils import TaskTypeEnum

METRICS_LOG_NAME = 'metrics_json.log'


class MetricsCollector:
    def __init__(self, log_name, conf: KFLConf):
        self.conf = conf
        self.__metrics_logs = []
        self.metrics_log = open(conf.metrics_dir + '/' + METRICS_LOG_NAME, 'w')

    def add_record(self, metrics: str):
        '''
        增加完整的一次指标记录：json字符串格式
        :param metrics: 如{’auc‘:0.9,'acc':0.98,'loss':12.09,'task':'train','glocb'}
        :return:
        '''
        self.__metrics_logs.append(metrics)
        self.metrics_log.write(metrics + '\n')
        self.metrics_log.flush()

    def close(self):
        self.metrics_log.close()


class Metrics(object):
    task: TaskTypeEnum = TaskTypeEnum.TRAIN
    global_step: int = None
    finish_pct: float = None

    auc = None
    acc = None
    f1 = None
    loss = None
    ndcg = None
    roc = None
    precision = None
    recall = None

    def __init__(self):
        pass


if __name__ == '__main__':
    m = Metrics()
