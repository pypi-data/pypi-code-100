#!/usr/bin/env python3
from setuptools import setup, find_packages

VERSION = '0.0.1'

required = []

setup(
    name='section9',
    version=VERSION,
    author='sunyi00',
    author_email='sunyi00@gmail.com',
    description='pypi/section9 package root',
    long_description='pypi/section9 package root',
    long_description_content_type="text/markdown",
    url='https://github.com/T-G-Family/section9',
    project_urls={
        "Bug Tracker": "https://github.com/T-G-Family/section9/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
