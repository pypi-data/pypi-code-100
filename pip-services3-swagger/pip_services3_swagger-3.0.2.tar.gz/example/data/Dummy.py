# -*- coding: utf-8 -*-
from pip_services3_commons.data import IStringIdentifiable


class Dummy(IStringIdentifiable):
    def __init__(self, id, key, content):
        self.id = id
        self.key = key
        self.content = content
