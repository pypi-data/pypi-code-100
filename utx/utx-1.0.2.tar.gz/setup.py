#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from utx import __version__

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="utx",
    version="{}".format(__version__),
    keywords=["utx", "airtest", "pytest", "selenium", "ui", "tools"],
    description='UTX will help you write ui automated tests more easily!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',

    url="https://github.com/openutx",
    author="lijiawei",
    author_email="jiawei.li2@qq.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    entry_points="""
    [console_scripts]
    utx = utx.cli.cli:main
    """,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["airtest~=1.2.2", "tenacity~=8.0.1", "allure-pytest~=2.9.43", "pocoui~=1.0.84",
                      "tidevice~=0.5.0", "faker~=4.18.0", "jmespath~=0.10.0", "loguru~=0.5.3", "pytest-xdist~=2.3.0",
                      "PyYAML~=5.4.1", "allure-python-commons~=2.9.43", "pytest-rerunfailures~=10.1", "imageio~=2.9.0",
                      "hexdump~=3.3", "pyOpenSSL~=21.0.0", "pyasn1~=0.4.8", "selenium~=3.14.0", "pynput~=1.7.4"]
)
