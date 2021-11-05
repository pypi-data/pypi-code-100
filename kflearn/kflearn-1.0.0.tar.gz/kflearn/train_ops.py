#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 15, 2021
'''
from kflearn.config_ops import KFLConf
from kflearn.model_ops import ModelInfo
from kflearn.constant_utils import ModelTypeEnum
import shutil
import os


class TrainContext(object):
    def __init__(self, conf: KFLConf = None):
        # self.conf = conf if conf is not None else KFLConf()
        self.conf = conf
        self.model_info = ModelInfo(self.conf)

    def get_data_tmp_dir(self):
        os.makedirs(self.conf.data_tmp_dir, exist_ok=True)
        return self.conf.data_tmp_dir

    def get_train_dir(self) -> str:
        os.makedirs(self.conf.train_dir, exist_ok=True)
        return self.conf.train_dir

    def get_valid_dir(self) -> str:
        os.makedirs(self.conf.valid_dir, exist_ok=True)
        return self.conf.valid_dir

    def get_test_dir(self) -> str:
        os.makedirs(self.conf.test_dir, exist_ok=True)
        return self.conf.test_dir

    def get_model_dir(self) -> str:
        os.makedirs(self.conf.model_dir, exist_ok=True)
        return self.conf.model_dir

    def get_metrics_dir(self) -> str:
        os.makedirs(self.conf.metrics_dir, exist_ok=True)
        return self.conf.metrics_dir

    def add_model_path(self, local_model_path):
        shutil.move(local_model_path, self.conf.model_dir)

    def auto_model_path(self, type: ModelTypeEnum) -> str:
        """自动生成模型path.
        :type 支持saved_model,checkpoint,pb,pmml等格式模型
        """
        os.makedirs(self.conf.model_dir, exist_ok=True)
        if type is ModelTypeEnum.SAVED_MODEL:
            return self.conf.model_dir + '/' + self.model_name()
        elif type is ModelTypeEnum.SINGLE_PB:
            return self.conf.model_dir + '/' + self.model_name() + '.pb'
        elif type is ModelTypeEnum.CHECKPOINT:
            return self.conf.model_dir + '/' + self.model_name()
        elif type is ModelTypeEnum.PMML:
            return self.conf.model_dir + '/' + self.model_name() + '.pmml'
        elif type is ModelTypeEnum.DIR:
            return self.conf.model_dir + '/' + self.model_name()
        else:
            raise Exception('模型类型参数异常')

    def model_name(self):
        return '_'.join([self.conf.train_name, self.conf.train_version, self.conf.train_algo_type])
