"""Response对象封装"""
import json
import re

from lxml import etree


class Response(object):
    def __init__(self, url, status_code, headers, body, meta={}):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.meta = meta

    def xpath(self, rule):
        '''xpath解析'''
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        '''json解析'''
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        '''findall正则'''
        if data is None:
            data = self.body
        return re.findall(rule, data)
