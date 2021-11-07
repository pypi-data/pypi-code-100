#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver


class WebDriver(EdgeWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        EdgeWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)
