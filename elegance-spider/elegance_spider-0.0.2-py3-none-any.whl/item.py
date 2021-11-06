"""Item对象"""


class Item(object):
    """
    Item对象
    """

    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        '''对外提供data访问'''
        return self._data
