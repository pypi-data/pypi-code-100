#!/usr/bin/env python3.6

import os
import io
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


root = os.path.dirname(__file__)
ver_py = os.path.join(root, 'tas_tools', 'version.py')
readme_path = os.path.join(root, 'README.rst')

try:
    with open(ver_py) as ver_py_file:
        ver_contents = ver_py_file.read()
    exec(ver_contents)
except FileNotFoundError:
    __version__ = "0.0.0.0"

with open(readme_path) as readme_file:
    readme_contents = readme_file.read()

setup(
    name='tas_tools',
    version=__version__,
    description='TaS tools, post-boot config files, and Axiom scripts',
    author='Ryan Heifferon',
    author_email='rheiffer@qti.qualcomm.com',
    long_description=readme_contents,
    license='proprietary, confidential, all rights reserved.',
    include_package_data=True,
    install_requires=[
        'paramiko',
        'pandas',
        'platformutil',
        'requests'
    ],
    packages=find_packages(),
    url='https://review-tbs.qualcomm.com/cgit/tbs/tas/tools'
)
