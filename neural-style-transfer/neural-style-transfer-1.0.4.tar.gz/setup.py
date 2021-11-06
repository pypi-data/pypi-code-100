import pathlib
import os
from setuptools import setup, find_packages
from setuptools.command.easy_install import easy_install
from distutils.util import convert_path

parent_path = pathlib.Path(__file__).parent
README = (parent_path / "README.md").read_text()
print(parent_path)
AUTHOR ='Divy Shah'
EMAIL = 'divyshah1712@gmail.com'

with open('/home/divy/Documents/Divy Shah/projects/neural-style-transfer/requirements.txt') as f:
    requirements = f.read().splitlines()

meta = {}
aboutPath = convert_path('neuralstyletransfer/about.py')
with open(aboutPath) as aboutFile:
    exec(aboutFile.read(), meta)

setup(
    name=meta['__title__'],
    version=meta['__version__'],
    description=meta['__summary__'],
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=requirements,
    author=meta['__author__'],
    author_email=EMAIL,
    license=meta['__license__']
)