#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = []

setup(
    name="vscodetest_pkg1",
    version="0.1.0",
    description="Python Boilerplate contains all the boilerplate you need"
    "to create a Python package.",
    long_description=readme,
    author="Md Nazrul Islam",
    author_email="email2nazrul@gmail.com",
    url="https://github.com/nazrulworld/vscodetest_pkg1",
    packages=["vscodetest_pkg1"],
    package_dir={"vscodetest_pkg1": "vscodetest_pkg1"},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords="vscodetest_pkg1",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
