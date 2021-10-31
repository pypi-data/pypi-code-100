#!/usr/bin/env python3

from setuptools import setup, find_packages
import alot_checkmail

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=alot_checkmail.__productname__,
    version=alot_checkmail.__version__,
    author=alot_checkmail.__author__,
    author_email=alot_checkmail.__author_email__,
    description=alot_checkmail.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=alot_checkmail.__url__,
    project_urls={
        "Bug Tracker": "{0}/issues".format(alot_checkmail.__url__),
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["alot"],
    packages=find_packages(exclude=['tests*']),
    provides=['alot_checkmail'],
    python_requires=">=3.6",
)
