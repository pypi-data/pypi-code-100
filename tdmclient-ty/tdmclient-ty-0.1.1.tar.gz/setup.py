# This file is part of tdmclient-ty
# Copyright 2021 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Miniature Mobile Robots group, Switzerland
# Author: Yves Piguet
#
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import find_packages, setup

with open("doc/help.md", "r") as f:
    long_description = f.read()

setup(
    name="tdmclient-ty",
    version="0.1.1",
    author="Yves Piguet",
    packages=["thonnycontrib.tdmclient_ty"],
    description="Communication with Thymio II robot from Thonny via the Thymio Device Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epfl-mobots/tdmclient-ty",
    install_requires=[
        "tdmclient",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Education",
    ],
    python_requires=">=3.6",
)
