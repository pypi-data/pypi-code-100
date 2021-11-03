#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


info = sys.version_info

setup(
    name='juyoshid_test01',
    version='1.1.0.0',
    description='Just test for PyPI.',
    long_description=readme,
    long_description_content_type='text/plain',
    author='juyoshid',
    author_email='*******@gmail.com',
    url='https://www.google.com/',
    packages=find_packages(),
    include_package_data=True,
    keywords='test',
    classifiers=[
	'Programming Language :: Python :: 3.9',
    ],
    entry_points = {
        'console_scripts': 
		['juyoshid_test01=juyoshid_test1.scripts.main:main'],
    },
)
