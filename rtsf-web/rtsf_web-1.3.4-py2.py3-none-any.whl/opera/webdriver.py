#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.opera.webdriver import WebDriver as OperaWebDriver


class WebDriver(OperaWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        OperaWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)

