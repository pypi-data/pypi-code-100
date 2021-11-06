#!/usr/bin/env python
# coding=utf-8

# from setuptools import setup, find_packages
from distutils.core import setup
from setuptools import find_packages

setup(
    name='t3tools',
    version='0.0.5',
    description=(
        '实用工具 from 唐峰2098'
    ),
    # long_description=open('README.rst').read(),
    long_description='common tools from tangfeng2098.',
    author='唐峰',
    author_email='tangfeng2098@outlook.com',
    maintainer='唐峰',
    maintainer_email='tangfeng2098@outlook.com',
    license='MIT License',
    packages=find_packages(),
    # packages=['common'],
    platforms=["all"],
    url='http://null.null.null',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)
