from setuptools import find_packages, setup
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='telebotify',
    packages=find_packages(),
    version='0.1.4',
    description='A Python library for developing Telegram bots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alejandro de Felipe',
    license='MIT',
    include_package_data=True,)
