#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.ie.webdriver import WebDriver as IeWebDriver


class WebDriver(IeWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        IeWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)
