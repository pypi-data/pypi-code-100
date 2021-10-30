import inspect
import time
from selenium.common.exceptions import TimeoutException
from qrunner.utils.log import logger
from qrunner.core.h5.driver import relaunch
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 安卓webview元素
class Element:
    def __init__(self, driver, *args, index=0):
        self.d = driver.d
        self.locator = args
        self.index = index
        self._element = None

    @relaunch
    def exists(self, timeout=3):
        try:
            WebDriverWait(self.d, timeout=timeout).until(EC.presence_of_element_located(self.locator))
            return True
        except TimeoutException:
            return False

    @relaunch
    def find_element(self, retry=3, timeout=3):
        self._element = self.d.find_elements(*self.locator)[self.index]
        while self.exists(timeout=timeout):
            if retry > 0:
                retry -= 1
                logger.info(f'重试 查找元素 {self.locator}')
                time.sleep(1)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】Not found element {self}')
                return None
        return self._element

    @relaunch
    @property
    def text(self):
        logger.info(f'获取元素文案: {self.locator}')
        element = self.find_element(retry=0)
        if element is None:
            raise AssertionError(f'未找到元素： {self.locator}')
        text = element.text
        logger.info(f'元素 {self.locator} 文案 {text}')
        return text

    @relaunch
    def click(self):
        logger.info(f'点击元素: {self.locator}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未找到元素： {self.locator}')



