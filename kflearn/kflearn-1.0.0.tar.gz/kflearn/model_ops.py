#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 19, 2021
'''
from kflearn.config_ops import KFLConf
from kflearn import file_util
from kflearn.constant_utils import ModelTypeEnum


class ModelInfo(object):
    def __init__(self, conf: KFLConf = None):
        self.conf = conf

    def auto_model_path(self, type: ModelTypeEnum) -> str:
        """自动生成模型path.
        :type 支持saved_model,checkpoint,pb,pmml等格式模型
        """
        file_util.create_dir_not_clear(self.conf.model_dir)
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
