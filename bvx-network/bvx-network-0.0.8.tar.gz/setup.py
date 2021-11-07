# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='bvx-network',
    version='0.0.8',
    description='Network utils.',
    author='Kazuhiro Kotsutsumi',
    url='https://github.com/kotsutsumi/bvx-network',
    packages=[
        'bvx_network',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
        'psutil~=5.8.0'
    ],
)