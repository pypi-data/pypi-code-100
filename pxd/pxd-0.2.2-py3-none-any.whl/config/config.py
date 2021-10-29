#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import configparser
import os
import platform

from deployer._repo import pxd_working_dir
from deployer.config.log_config import setup_logging
from deployer.config.metadb_config import setup_metadb


class Config:
    _instance = None

    # DOCKER_REPO_URL = "registry.cn-zhangjiakou.aliyuncs.com/drds_pre/"
    DOCKER_REPO_URL = "polardbx/"

    CN_IMAGE_NAME = "galaxysql"
    DN_IMAGE_NAME = "galaxyengine"
    CDC_IMAGE_NAME = "galaxycdc"

    CN_IMAGE_VERSION = 'latest'
    DN_IMAGE_VERSION = "latest"
    CDC_IMAGE_VERSION = "latest"

    CN_TOOL_IMAGE_NAME = "polardbx-init"
    CN_TOOL_IMAGE_VERSION = 'latest'

    DN_TOOL_IMAGE_NAME = "xstore-tools"
    DN_TOOL_IMAGE_VERSION = "latest"
    
    run_host = None


    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def instance():
        return Config()

    @classmethod
    def load_config(cls, *args, **kwargs):
        pxd_config_file = pxd_working_dir + '/config'
        if os.path.exists(pxd_config_file):
            config = configparser.RawConfigParser()
            config.optionxform = lambda option: option
            config.read(pxd_config_file)
            for section_name, sections in config.items():
                for key, value in sections.items():
                    if hasattr(cls.instance(), key):
                        cls.instance().__setattr__(key, value)
        for key, value in kwargs.items():
            if value:
                cls.instance().__setattr__(key, value)

    @property
    def all_polardbx_images(self):
        return [
            self.cn_image,
            self.cn_tool_image,
            self.dn_image,
            self.dn_tool_image,
            self.cdc_image
        ]

    @property
    def cn_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CN_IMAGE_NAME}:{self.CN_IMAGE_VERSION}'

    @property
    def cn_tool_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CN_TOOL_IMAGE_NAME}:{self.CN_TOOL_IMAGE_VERSION}'

    @property
    def dn_image(self):
        return f'{self.DOCKER_REPO_URL}{self.DN_IMAGE_NAME}:{self.DN_IMAGE_VERSION}'

    @property
    def dn_tool_image(self):
        return f'{self.DOCKER_REPO_URL}{self.DN_TOOL_IMAGE_NAME}:{self.DN_TOOL_IMAGE_VERSION}'

    @property
    def cdc_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CDC_IMAGE_NAME}:{self.CDC_IMAGE_VERSION}'

    @staticmethod
    def host_network_support():
        """
        Docker for mac is run on a virtual machine, so only 'bridge' mode is supported
        :return: Return false is platform is Darwin, otherwise return true.
        """
        if Config.instance().run_host == '127.0.0.1':
            return False
        if platform.system() in ("Darwin", "Windows"):
            return False
        return True



def setup_pxd_context():
    setup_pxd_working_dir()
    setup_logging()
    setup_metadb()


def setup_pxd_working_dir():
    if os.path.exists(pxd_working_dir):
        return
    os.makedirs(pxd_working_dir, exist_ok=True)
