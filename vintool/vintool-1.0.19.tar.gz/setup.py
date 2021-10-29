#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: vincent
# Mail: long_ty@163.com
# Created Time:  2021-03-19 14:55:42
# python3 setup.py sdist
# twine upload dist/*
#############################################


from setuptools import setup, find_packages

setup(
    name="vintool",
    version="1.0.19",
    keywords=("tools"),
    description="tools",
    long_description="http,env,oss,mq",
    license="MIT Licence",
    python_requires=">=3.6",

    url="https://github.com/fengmm521/pipProject",
    author="vincent",
    author_email="long_ty@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'ffmpy==0.3.0',
        'pika==1.2.0',
        'retry==0.9.2',
        'requests==2.25.1',
        # 'qcloud_cos==3.3.6',
    ]
)
