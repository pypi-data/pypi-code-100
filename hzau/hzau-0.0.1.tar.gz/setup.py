#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='hzau',
    version='0.0.1',
    author='Chang-LeHung',
    author_email='chang-lehung@gmail.com',
    url='https://github/Chang-LeHung',
    description=u'utis',
    packages=['hzau'],
    install_requires=['torch', 'matplotlib', 'numpy', 'seaborn',
                      'sys', 'torchvision', 'IPython']
)