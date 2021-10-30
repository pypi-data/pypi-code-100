import os

import requests
from selenium import webdriver
from qrunner.utils.log import logger
from conf.config import conf
from qrunner.core.android.element import driver


# 重启chromedriver的装饰器
def relaunch(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.ConnectionError as _:
            logger.warning("chromedriver error, relaunch now.")
            self.d = Driver().d
    return wrapper


class Driver(object):
    # _instance = {}
    #
    # def __new__(cls, serial_no=None):
    #     if serial_no not in cls._instance:
    #         cls._instance[serial_no] = super().__new__(cls)
    #     return cls._instance[serial_no]

    def __init__(self, serial_no=None, pkg_name=None):
        if not serial_no:
            self.serial_no = conf.get_name('device', 'serial_no')
        else:
            self.serial_no = serial_no
        if not pkg_name:
            self.pkg_name = conf.get_name('app', 'pkg_name')

        logger.info(f'启动webdriver')
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('androidDeviceSerial', self.serial_no)
        # options.add_experimental_option('androidPackage', self.pkg_name)
        # options.add_experimental_option('androidUseRunningApp', True)
        # options.add_experimental_option('androidProcess', self.pkg_name)
        exe_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../libs/chromedriver', '91', 'chromedriver.exe')
        logger.info(f'chromedriver路径: {exe_path}')
        self.d = webdriver.Chrome(executable_path=exe_path, options=options)
        self.d.set_page_load_timeout(10)

    @relaunch
    def back(self):
        logger.info('返回上一页')
        self.d.back()

    @relaunch
    def send_keys(self, value):
        logger.info(f'输入文本: {value}')
        driver.send_keys(value)

    @relaunch
    def screenshot(self, filename, timeout=3):
        driver.wait_shot(filename, timeout=timeout)

    @relaunch
    def get_ui_tree(self):
        page_source = self.d.page_source()
        logger.info(f'获取页面内容: \n{page_source}')
        return page_source

    @relaunch
    def get_windows(self):
        logger.info(f'获取当前打开的窗口列表')
        return self.d.window_handles

    @relaunch
    def switch_window(self, old_windows):
        logger.info('切换到最新的window')
        current_windows = self.get_windows()
        newest_window = [window for window in current_windows if window not in old_windows][0]
        self.d.switch_to.window(newest_window)

    @relaunch
    def close(self):
        logger.info('关闭webdriver')
        self.d.close()

    @relaunch
    def execute_js(self, script, element):
        logger.info(f'执行js脚本: \n{script}')
        self.d.execute_script(script, element)


# 初始化
driver = Driver()
d = driver.d





