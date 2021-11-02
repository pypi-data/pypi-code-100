import sys
import os
import setuptools
import setuptools.command.build_py
import distutils.cmd
import distutils
from distutils.core import setup, Extension
import distutils.log
import distutils.log
distutils.log.set_verbosity(distutils.log.INFO)

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="apex_markets",
    version="0.0.4",
    author="Apex Markets",
    author_email="ljwcharles@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    keywords="apex python client",
)
