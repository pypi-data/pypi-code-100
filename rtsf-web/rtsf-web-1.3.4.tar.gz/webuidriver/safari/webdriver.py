#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver


class WebDriver(SafariWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        SafariWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)

