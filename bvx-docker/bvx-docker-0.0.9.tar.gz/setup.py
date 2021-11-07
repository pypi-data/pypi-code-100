# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='bvx-docker',
    version='0.0.9',
    description='docker helpers.',
    author='Kazuhiro Kotsutsumi',
    url='https://github.com/kotsutsumi/bvx-docker',
    packages=[
        'bvx_docker',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
        'docker~=5.0.3'
    ],
)

# EOF
