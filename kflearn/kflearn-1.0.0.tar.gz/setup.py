#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 11 04, 2021
'''
from setuptools import setup, find_packages
import requests
import os


def md_to_rst(from_file, to_file):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(from_file, 'rb')}
    )

    if response.ok:
        with open(to_file, "wb") as f:
            f.write(response.content)


# md_to_rst("README.md", "README.rst")

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='kflearn',
    version='1.0.0',
    description='machine learning kit for algorithm train platform',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author='horn',
    author_email='hongen26@163.com',
    url='https://code.amh-group.com/model-platform/kflearn',
    license='MIT Licence',
    keywords='ga nn',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    # packages=['kflearn'],
    packages=find_packages(),
    install_requires=[],  # 'numpy>=1.14', 'tensorflow>=1.7'
    python_requires='>=3'
)
