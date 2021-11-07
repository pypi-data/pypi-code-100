#! python3
# -*- encoding: utf-8 -*-

from webuidriver.remote.wait_until import WaitUntil
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver


class WebDriver(ChromeWebDriver, WaitUntil):
    def __init__(self, *args, **kwargs):
        ChromeWebDriver.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)
