#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from os.path import dirname, abspath, join


def get_static():
    """
    获取静态资源路径
    """
    dirname_root = dirname(dirname(abspath(__file__)))
    return join(dirname_root, "static")
