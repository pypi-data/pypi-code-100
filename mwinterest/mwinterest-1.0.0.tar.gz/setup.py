#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/11/5
@Author  ：mosowong
@File    ：setup.py
@Version ：1.0.0
@Function：打包项目
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mwinterest', #包名
    version='1.0.0', #版本号
    author='mosowong', #作者
    author_email='mosowong@163.com', #邮箱
    description='MosoWong Interest Series', #概述
    url='', #项目地址
    packages=find_packages(), #包的列表
    long_description=long_description, #项目描述
    long_description_content_type="text/markdown", #描述文档
    python_requires='>=3.10.0', #版本约束
    install_requires=[], #其他约束
    license="GPLv3", #开源协议
    #许可证连接
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
)
