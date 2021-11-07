#! python3
# -*- encoding: utf-8 -*-

import os
from selenium.webdriver import FirefoxProfile as BaseFirefoxProfile


class FirefoxProfile(BaseFirefoxProfile):

    def __init__(self, ):
        super(FirefoxProfile, self).__init__()

    def set_download(self, download_path, file_types, folder_type=2, is_show=False):
        """
        :param download_path:  指定下载路径
        :param file_types:     对所给出文件类型不再弹出框进行询问,直接下载，逗号隔开, 例如：
                                    'application/octet-stream, application/zip,application/gzip'
        :param folder_type:    设置Firefox的默认 下载 文件夹。0是桌面；1是“我的下载”；2是自定义
        :param is_show:        在开始下载时是否显示下载管理器,  True/False
        :return: None
        """

        if not os.path.isdir(download_path):
            raise ValueError("Download path is not a valid directory path.")

        self.set_preference("browser.download.dir", download_path)
        self.set_preference("browser.download.folderList", folder_type)
        self.set_preference("browser.download.manager.showWhenStarting", False)
        self.set_preference("browser.helperApps.neverAsk.saveToDisk", file_types)
