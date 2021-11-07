from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'Modulo con definiciones de la DIAN'

PACKAGE_NAME = "docedian"

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/pedroporras/dian_technical_data',
    author='Pedro Porras',
    author_email='<pedroporras@inexpresivo.com>',
    keywords=['DIAN', 'Colombia'],
    license='LGPL',
    packages=find_packages(),
    install_requires = [],
    extras_require = {
        'dev': [],
        'test': [],
    },
)
