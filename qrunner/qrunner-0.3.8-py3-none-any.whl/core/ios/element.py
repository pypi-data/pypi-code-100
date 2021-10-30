import inspect
import time
from qrunner.core.ios.driver import d, relaunch_wda
from qrunner.utils.log import logger


class Element:
    def __init__(self, **kwargs):
        self.index = kwargs.pop('index', 0)
        self.xpath = kwargs.get('xpath', '')
        self._kwargs = kwargs
        self._element = None

    @relaunch_wda
    def find_element(self, retry=3, timeout=3):
        self._element = d.xpath(self.xpath) if self.xpath else d(**self._kwargs)[self.index]
        while not self._element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                logger.warning(f'重试 查找元素： {self._kwargs}')
                time.sleep(2)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】未找到元素 {self._kwargs}')
                return None
        return self._element

    @relaunch_wda
    def attr(self, name):
        logger.info(f'元素 {self._kwargs}-{name} 属性:')
        element = self.find_element(retry=0)
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        _info = None
        if name == 'info':
            _info = element.info
        elif name == "count":
            _info = element.count()
        elif name == 'id':
            _info = element.id
        elif name == 'name':
            _info = element.name
        elif name == 'label':
            _info = element.label
        elif name == 'value':
            _info = element.value
        elif name == 'text':
            _info = element.text
        elif name == 'className':
            _info = element.className
        elif name == "accessibilityContainer":
            _info = element.accessibilityContainer
        elif name == "accessible":
            _info = element.accessible
        elif name == 'visible':
            _info = element.visible
        elif name == "enabled":
            _info = element.enabled
        elif name == "displayed":
            _info = element.displayed
        elif name == "bounds":
            _info = element.bounds
        logger.info(_info)
        return _info

    # 用于常见分支场景判断
    @property
    @relaunch_wda
    def exists(self):
        logger.info(f'元素 {self._kwargs} 是否存在:')
        _exist = self.find_element(retry=0, timeout=1) is not None
        logger.info(_exist)
        return _exist

    @relaunch_wda
    def tap(self):
        logger.info(f'点击元素: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()
        logger.info('点击成功')

    @relaunch_wda
    def input(self, text, clear=True):
        logger.info(f'输入框 {self._kwargs} 输入: {text}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()
        if clear:
            element.clear_text()
        element.set_text()
        logger.info('输入成功')





