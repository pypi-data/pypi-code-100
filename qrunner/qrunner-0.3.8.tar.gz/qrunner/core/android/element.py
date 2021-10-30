import inspect
import time
from qrunner.utils.log import logger
from qrunner.core.android.driver import driver, d


# 安卓原生元素
class Element:
    def __init__(self, **kwargs):
        self.index = kwargs.pop('index', 0)
        self.xpath = kwargs.get('xpath', '')
        self._kwargs = kwargs
        self._element = None

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

    def attr(self, name):
        logger.info(f'元素 {self._kwargs}-{name} 属性:')
        element = self.find_element(retry=0)
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        _info = None
        if name == 'info':
            _info = element.info
        if name == "count":
            _info = element.count
        elif name == 'resourceId':
            _info = element.info.get('resourceName')
        elif name == 'text':
            _info = element.info.get('text')
        elif name == 'packageName':
            _info = element.info.get('packageName')
        elif name == 'className':
            _info = element.info.get('className')
        elif name == 'description':
            _info = element.info.get('contentDescription')
        elif name == 'bounds':
            _info = element.info.get('bounds')
        elif name == "visibleBounds":
            _info = element.info.get('visibleBounds')
        elif name == "childCount":
            _info = element.info.get('childCount')
        elif name == 'checkable':
            _info = element.info.get('checkable')
        elif name == "checked":
            _info = element.info.get('checked')
        elif name == "clickable":
            _info = element.info.get('clickable')
        elif name == "enabled":
            _info = element.info.get('enabled')
        elif name == "focusable":
            _info = element.info.get('focusable')
        elif name == "focused":
            _info = element.info.get('focused')
        elif name == "longClickable":
            _info = element.info.get('longClickable')
        elif name == "scrollable":
            _info = element.info.get('scrollable')
        elif name == "selected":
            _info = element.info.get('selected')
        logger.info(_info)
        return _info

    # 用于常见分支场景判断
    @property
    def exists(self):
        logger.info(f'判断元素是否存在: {self._kwargs}')
        return self.find_element(retry=0, timeout=1) is not None

    def tap(self):
        logger.info(f'点击元素: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()

    def input(self, text, clear=True):
        logger.info(f'定位元素并输入{text}: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()
        d.send_keys(str(text), clear=clear)
        d.send_action('search')
        d.set_fastinput_ime(False)





