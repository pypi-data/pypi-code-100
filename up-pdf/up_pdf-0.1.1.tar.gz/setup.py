
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name='up_pdf',
    version='0.1.1',
    author='White.tie',
    author_email='1042798703@qq.com',
    url='https://github.com/tyj-1995',
    description='up pdf file to ali cloud',
    long_description='上传pdf到阿里云,up pdf file to ali cloud',
    packages=['up_pdf'],
    install_requires=['requests'],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 3.6",
        ],
)
