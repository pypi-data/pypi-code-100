from pyfonybundles.Bundle import Bundle


class Bundle1(Bundle):
    pass


class Bundle2(Bundle):
    pass


class EntryPointMocked:
    def __init__(self, bundle_class):
        self.__bundle_class = bundle_class

    def load(self):
        return self.__bundle_class
