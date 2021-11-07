# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='bvx-oop',
    version='0.0.9',
    description='Object-Oriented Programming classes.',
    author='Kazuhiro Kotsutsumi',
    url='https://github.com/kotsutsumi/bvx-oop',
    packages=[
        'bvx_oop',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
    ],
)

# EOF
