#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 26, 2021
'''

import yaml
import logging
import os
# from deprecated.sphinx import deprecated
import warnings

this_dir = os.path.dirname(__file__)
root_dir = os.getcwd()


class KFLConf(object):
    def __init__(self, yaml_path=root_dir + '/kfl_config.yaml'):
        self.yaml_path = yaml_path

        conf_file = open(self.yaml_path, encoding='utf8')
        self.conf = yaml.load(conf_file, Loader=yaml.FullLoader)

    def set(self, field=None, conf_key=None, conf_value=None):
        if field not in self.conf:
            self.conf[field] = {conf_key: conf_value}
        else:
            self.conf[field][conf_key] = conf_value
        return self

    def get(self, field=None, conf_key=None):
        return self.conf[field][conf_key]

    def dump(self, path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.conf, f)

    def build(self):
        '''
        根据config.yaml初始化基础配置，新建目录等
        :return:
        '''
        self.train_name = self.conf['info']['trainName']
        self.train_version = self.conf['info']['trainVersion']
        self.train_algo_type = self.conf['info']['trainAlgoType']

        self.data_tmp_dir = os.path.join(root_dir, self.conf['data']['dataTmp']['dir'])
        self.train_dir = os.path.join(root_dir, self.conf['data']['trainData']['dir'])
        self.valid_dir = os.path.join(root_dir, self.conf['data']['validData']['dir'])
        self.test_dir = os.path.join(root_dir, self.conf['data']['testData']['dir'])
        self.metrics_dir = os.path.join(root_dir, self.conf['data']['metricsLog']['dir'])
        self.model_dir = os.path.join(root_dir, self.conf['data']['modelData']['dir'])

        logging.info('#### Yaml配置信息：' + str(self.conf))
        self.dump(self.yaml_path)
        return self

    # @deprecated
    def set_kv(self, conf_key=None, conf_value=None, conf_dict: dict = None):
        warnings.warn("set_f is not recommended", DeprecationWarning)

        if conf_key is not None and conf_value is not None:
            self.conf[conf_key] = conf_value
        elif conf_dict is not None:
            self.conf.update(conf_dict)
        else:
            raise Exception('配置输入参数异常')
        return self

    # @deprecated
    def set_list(self, conf_keys: list = None, conf_value=None):
        warnings.warn("set_list is not recommended", DeprecationWarning)

        val = conf_value
        for key in conf_keys[::-1]:
            val = {key: val}

        outer1 = self.conf
        outer2 = val
        for key in conf_keys:
            if key not in outer1:
                outer1.update(outer2)
                break
            else:
                outer1 = outer1[key]
                outer2 = outer2[key]

        print(val)
        self.conf = val
        return self


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    conf = KFLConf()
    # conf.set('auth', 'horn').build()
