#!/usr/bin/env python
#  Copyright (c) 2021 Henning Janssen
#
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "pyyaml"
]

setup(
    author='Henning Janssen',
    author_email='janssen@eeh.ee.ethz.ch',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description=(
        'This package provides a simple notifier sending emails'
    ),
    entry_points={},
    python_requires='>=3.7',
    install_requires=requirements,
    license='GNU General Public License v3',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords='simple_email_sender',
    name='simple_email_sender',
    packages=find_packages(),
    url='https://gitlab.com/hjanssen/simple-email-sender',
    version='0.0.1',
    zip_safe=False,
)
