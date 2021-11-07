#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver


class WebDriver(FirefoxWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        FirefoxWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)
