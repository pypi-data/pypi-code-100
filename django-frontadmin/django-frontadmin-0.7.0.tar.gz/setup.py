#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='django-frontadmin',
    version='0.7.0',
    author='Washim Ahmed',
    author_email='washim.ahmed@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/washim/django-frontadmin',
    license='MIT',
    description='Frontadmin is a Django app to conduct Web-based frontend theme.',
    long_description=long_description,
    include_package_data=True,
    install_requires=[
        'django',
    ],
    python_requires='>=3.6',
)