#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 15, 2021
'''

from enum import Enum


class AlgTypeEnum(Enum):
    TENSORFLOW_V1 = "tensorflow1.x"
    TENSORFLOW_V2 = "tensorflow2.x"
    TORCH = "torch"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"


class TensorflowModelTypeEnum(Enum):
    SAVED_MODEL = "saved_model"
    CHECKPOINT = "ckpt"


class ModelTypeEnum(Enum):
    SAVED_MODEL = 1  # 模型是saved_model api 生成
    CHECKPOINT = 2  # 模型是TensorFlow的save生成
    PMML = 3  # 模型是单个.pmml文件
    SINGLE_PB = 4  # 模型是单个.pb文件
    DIR = 5  # 模型就是个目录


class TaskTypeEnum(Enum):
    TRAIN = 'train'
    VALID = 'valid'
    TEST = 'test'
    INFER = 'infer'


class MeticsEnum(Enum):
    AUC = 'auc'
    ACC = 'acc'
    ROC = 'roc'
    F1 = 'f1'
    LOSS = 'loss'
    NDCG = 'ndcg'
    PRECISION = 'precision'
    RECALL = 'recall'
