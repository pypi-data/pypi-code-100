# Author: AmarnathCJD
# Project: py-cryptocurrency

import os
import re
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


version = "1.1"

setup(
    name='py-cryptocurrency',
    version=version,
    description='Wrapper to get real time cypto currency values',
    url='https://github.com/AmarnathCJD/py-cryptocurrency',
    author='AmarnathCJD',
    author_email='AmarnathCJD@users.noreply.github.com',
    license='GNU',
    packages=find_packages(),
    download_url=f"https://github.com/AmarnathCJD/py-cryptocurrency/releases/tag/{version}",
    keywords=['py', 'crypto', 'currency'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ]
)
