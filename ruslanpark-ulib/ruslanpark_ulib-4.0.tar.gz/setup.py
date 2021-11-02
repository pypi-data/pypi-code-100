from setuptools import setup, find_packages
from os.path import join, dirname
import ruslanpark_ulib

setup(
    name='ruslanpark_ulib',
    version='4.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=['numpy<1.0'],
)