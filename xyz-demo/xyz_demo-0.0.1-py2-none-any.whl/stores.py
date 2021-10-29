# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_util.mongoutils import Store

class ObjectLog(Store):
    name = 'object_log'
    timeout = 1000
