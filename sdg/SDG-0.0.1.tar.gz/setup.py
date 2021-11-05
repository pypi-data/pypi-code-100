#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    name='SDG',
    version='0.0.1',
    description='Synthetic Data Generation (SDG) for tabular data and time series',
    author='Yi Zhang',
    author_email='yizhang.dev@gmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/imyizhang/SDG',
    download_url='https://github.com/imyizhang/SDG',
    packages=setuptools.find_packages(),
    keywords=[
        'sdg', 'generative-adversarial-network', 'synthetic-data-generation',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'torch>=1.8.1'
    ],
)
