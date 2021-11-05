from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

setup(
    name='namespace_kube',
    packages=["namespace_kube"],
    include_package_data=True,
    version='0.1.0',
    description='find namespace in running pod',
    author='YYT',
    license='MIT',
)