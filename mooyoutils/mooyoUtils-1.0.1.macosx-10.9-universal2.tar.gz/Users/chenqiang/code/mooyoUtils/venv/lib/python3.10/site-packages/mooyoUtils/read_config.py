# -*- coding: UTF-8 -*-

import os
from .logger import logger
from .pyapollo import ApolloClient

proDir = os.path.split(os.path.realpath(__file__))[0]

env, idc = os.getenv('ENV'), os.getenv('IDC')
APOLLO_META, APOLLO_APP_ID = os.getenv('APOLLO_META'), os.getenv('APP_ID')

env = env and env.lower()
idc = idc and idc.lower()

if env not in ('fat', 'uat', 'pro'):
    logger.error('env[%s] 不能被识别, 设置为默认值 local' % env)
    env = 'local'
else:
    logger.info('get env[%s]' % env)

if idc not in ('id', 'ph', 'vn', 'default', 'uat', 'inscredit', 'uat-inscredit'):
    logger.error('idc[%s] 不能被识别, 设置为默认值 local' % idc)
    idc = 'local'
else:
    logger.info('get idc[%s]' % idc)

logger.info(f'Start Up! ENV[{env}], IDC[{idc}], APOLLO_META[{APOLLO_META}], APOLLO_APP_ID[{APOLLO_APP_ID}]')


class ApolloConfigReader:
    def __init__(self):
        app_id = APOLLO_APP_ID

        cluster = idc
        url = APOLLO_META
        logger.info('app_id[%s], cluster[%s], url[%s]' % (app_id, cluster, url))

        self.apollo_client = ApolloClient(app_id=app_id, cluster=cluster, config_server_url=url)
        self.apollo_client.start()
        self.base_path, self.env = proDir, env
        self.global_params = {'env': self.env, 'base_path': self.base_path}

    def get_configurations(self):
        return self.apollo_client.get_configurations()

    def get_value(self, key):
        if key in self.global_params:
            return self.global_params.get(key)
        return self.apollo_client.get_value(key)

    def set_params(self, key, value):
        self.global_params[key] = value

    def is_allow_env(self, *args, **kwargs):
        if self.env in set(args):
            return True
        else:
            logger.info('Env[%s] is not allowed.' % self.env)


# 读取Apollo配置
apollo_reader = ApolloConfigReader()
