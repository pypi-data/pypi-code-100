# -*- coding: utf-8 -*-
#!/usr/bin/env python
from io import open

from setuptools import find_packages, setup

from jwt_utils.meta import VERSION


setup(
    name='pyjwt-utils',
    version=str(VERSION),
    description='PyJwt-Utils is a wrapper to facility your token encode/decode',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Shinneider Libanio da Silva',
    author_email='shinneider-libanio@hotmail.com',
    url='https://github.com/shinneider/pyjwt-utils',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires=">=3.3",
    install_requires=[
        'pyjwt',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
