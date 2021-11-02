#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: tr3tty
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 tr3tty
"""

version = '1.0.0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='avtf_api_joke',
    version=version,

    author='tr3tty',
    author_email='vadim.ivanov13371@gmail.com',

    description=(
        u'Python module for avtf'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['avtf_api_joke'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)