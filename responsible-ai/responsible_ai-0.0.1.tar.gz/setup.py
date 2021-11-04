# Copyright (c) 2021 Massachusetts Institute of Technology
# SPDX-License-Identifier: MIT

from setuptools import find_packages, setup

DISTNAME = "responsible_ai"
LICENSE = "MIT"
AUTHOR = "Justin Goodwin, Ryan Soklaski"
AUTHOR_EMAIL = "ryan.soklaski@gmail.com"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering",
]
KEYWORDS = "AI pytorch machine learning robustness adversarial metrics calibration"
INSTALL_REQUIRES = []
TESTS_REQUIRE = []

DESCRIPTION = "Creating and verifying robust AI systems"


setup(
    name=DISTNAME,
    version="0.0.1",
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    description=DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    python_requires=">=3.6",
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
)
