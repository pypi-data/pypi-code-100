# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tsmock']
setup_kwargs = {
    'name': 'tsmock',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Erik Aronesty',
    'author_email': 'erik@atakama.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.8',
}


setup(**setup_kwargs)
