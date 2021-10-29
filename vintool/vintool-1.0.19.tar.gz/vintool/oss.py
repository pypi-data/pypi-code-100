#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging
from . import env

inst = dict()


def upload(local, target, **kwargs):
    return __get_instance(**kwargs).upload(local, target, **kwargs)


def download(key, save_path, **kwargs):
    return __get_instance(**kwargs).download(key, save_path, **kwargs)


def list_objects(path, **kwargs):
    return __get_instance(**kwargs).list_objects(path, **kwargs)


def __get_instance(**kwargs):
    global inst
    if 'config' in kwargs:
        option = kwargs['config']
    else:
        option = 'oss'

    if 'driver' in kwargs:
        driver = kwargs['driver']
    else:
        driver = env.get(option + '.driver')

    if not driver: driver = 'Cos'  # 未定义，默认为Cos

    driver = driver.capitalize()
    if option not in inst:
        logging.getLogger(__name__).info('Init %s:%s' % (driver, option))
        options = env.get(option)
        inst[option] = globals()[driver](options)
    return inst[option]


class BaseOss(object):
    def __init__(self, options):
        self.options = dict()
        if options: self.options = dict(self.options, **options)

    def download(self, key, save_path=None, **kwargs):
        raise NotImplementedError

    def upload(self, local, target, **kwargs):
        raise NotImplementedError

    def list_objects(self, path, **kwargs):
        raise NotImplementedError

    def option(self, key, default=None):
        if key.find('.') < 0:
            if key in self.options:
                return self.options[key]
            else:
                return default
        else:
            keys = key.split('.')
            if keys[0] in self.options and keys[1] in self.options[keys[0]]:
                return self.options[keys[0]][keys[1]]
            else:
                return default


class Cos(BaseOss):
    def __init__(self, options):
        # 引入cos sdk
        from qcloud_cos import CosConfig, CosS3Client

        super().__init__(options)
        self.options = {
            'region': 'ap-guangzhou',
            'bucket': None,
            'secret_id': None,
            'secret_key': None,
        }
        if options: self.options = dict(self.options, **options)
        cfg = CosConfig(Region=self.option('region'), SecretId=self.option('secret_id'),
                        SecretKey=self.option('secret_key'), Token=None)
        self.client = CosS3Client(cfg)

    def download(self, key, save_path=None, **kwargs):
        # 默认为源文件名称
        if save_path is None:
            save_path = os.path.basename(key)
        # 自动创建目录
        folder = os.path.dirname(save_path)
        if folder and not os.path.isdir(folder): os.makedirs(folder)

        # replace=0,则不重复下载
        if 'replace' in kwargs and not kwargs['replace'] and os.path.isfile(save_path): return save_path
        response = self.client.get_object(self.options['bucket'], key)
        logging.getLogger(__name__).info('cos download response => %s' % response)
        response['Body'].get_stream_to_file(save_path)
        return save_path

    def upload(self, path, target, **kwargs):
        response = self.client.put_object_from_local_file(self.option('bucket'), path, target)
        logging.getLogger(__name__).info('cos upload response => %s' % response)

    def list_objects(self, path, **kwargs):
        return self.client.list_objects(self.option('bucket'), path)
