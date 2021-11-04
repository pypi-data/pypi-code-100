#!/usr/bin/env python
# -*-coding utf-8 -*-

""" The setup script """

from setuptools import setup, find_packages

setup(
    name='mysvm',
    author='aleck fang',
    author_email='mail.fangzheng@gmail.com',
    maintainer='aleck fang',
    maintainer_email='mail.fangzheng@gmail.com',
    description='this is a python3 library',
    license='MIT',
    install_requires=[
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'abc=mysvm:main'
        ]
    },
    version='0.0.1',
    scripts=[],
)