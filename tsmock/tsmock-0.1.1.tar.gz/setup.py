# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tsmock']
setup_kwargs = {
    'name': 'tsmock',
    'version': '0.1.1',
    'description': 'Thread safe wrapper around unittest.mock',
    'long_description': None,
    'author': 'Erik Aronesty',
    'author_email': 'erik@atakama.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AtakamaLLC/tsmock',
    'py_modules': modules,
    'python_requires': '>=3.6.8',
}


setup(**setup_kwargs)
