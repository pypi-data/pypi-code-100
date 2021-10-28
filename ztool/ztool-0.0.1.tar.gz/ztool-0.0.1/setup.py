#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:     御风

import os
import setuptools

version = "0.0.1"

long_description = ""
if os.path.exists("readme.md"):
    with open("readme.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setuptools.setup(
    name="ztool",
    version=version,
    url="https://pypi.org/project/ztool/",

    author="Zhong Yufeng",
    author_email="zhong.yufeng@foxmail.com",

    description="ToolBox for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",

    license="MIT",

    # 模块相关元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],

    # 自动找到项目中导入的模块
    packages=setuptools.find_packages(),

    # 依赖模块
    install_requires=[
    ],

    # 依赖平台
    platforms="any",

    # 依赖 python 版本
    python_requires=">=3",
)
