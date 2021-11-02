#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup
from setuptools import find_packages

setup(
    name='KcangNacos',
    version='1.7',
    description=(
        '便捷python使用naocs构建微服务，并提供一个负载均衡的服务调用方法'
    ),
    long_description=open('README.rst').read(),
    author='kcangYan',
    author_email='842762472@qq.com',
    maintainer='kcangYan',
    maintainer_email='842762472@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/KcangYan/nacos-python-sdk',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)