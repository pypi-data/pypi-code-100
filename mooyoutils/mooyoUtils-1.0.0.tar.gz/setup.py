# -*- coding: UTF-8 -*-
# @Time     : 2021/11/4 13:56
# @Author   : Jackie
# @File     : setup.py

# coding: utf-8

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    sys.exit('Python 3.5 or greater is required.')


with open('README.md', 'rb') as fp:
    readme = fp.read()

# 版本号，自己随便写
VERSION = "1.0.0"

LICENSE = "MIT"

setup(
    name='mooyoUtils',
    version=VERSION,
    description='mooyo 常用工具包',
    long_description=readme,
    author='Jackie Chen',
    author_email='mooyo@live.cn',
    maintainer='Jackie Chen',
    maintainer_email='mooyo@live.cn',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='http://git.ppdaicorp.com/chenqiang08/mooyoUtils.git',
    install_requires=['portion', 'demjson', 'python-dateutil', 'paramiko', 'redis', 'jsonpath', 'pymysql',
                      'apscheduler', 'requests', 'gnupg', 'xlrd'],
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

# URL 你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
# INSTALL_REQUIRES 模块所依赖的python模块
# 以上字段不需要都包含
