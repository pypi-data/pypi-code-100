# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='bvx-docker',
    version='0.0.8',
    description='Object-Oriented Programming classes.',
    author='Kazuhiro Kotsutsumi',
    url='https://github.com/kotsutsumi/bvx-docker',
    packages=[
        'bvx_docker',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
    ],
)