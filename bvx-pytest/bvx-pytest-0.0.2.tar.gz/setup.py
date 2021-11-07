# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='bvx-pytest',
    version='0.0.2',
    description='pytest helpers.',
    author='Kazuhiro Kotsutsumi',
    url='https://github.com/kotsutsumi/bvx-pytest',
    packages=[
        'bvx_pytest',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
        'bvx-docker', 'bvx-network'
    ],
)

# EOF
