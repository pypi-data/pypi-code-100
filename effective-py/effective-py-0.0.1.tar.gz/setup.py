#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from collections import OrderedDict
from setuptools import setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('effective_py/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='effective-py',
    version=version,
    url='https://github.com/mikezone/effective-py',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/mikezone/effective-py'),
        ('Code', 'https://github.com/mikezone/effective-py'),
        ('Issue tracker', 'https://github.com/mikezone/effective-py/issues'),
    )),
    license='MIT',
    author='mike_chang',
    author_email='82643885@qq.com',
    maintainer='mike_chang',
    maintainer_email='82643885@qq.com',
    description='Extension for Python simulate other program language',
    long_description=readme,
    packages=['effective_py'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,>=3.7',
    install_requires=[
        'six>=1.16.0'
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
