# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['soe']
setup_kwargs = {
    'name': 'soe',
    'version': '0.0.5',
    'description': 'This library is needed to manage the operating system. It contains the functions of the os, sys, psutil module.',
    'long_description': None,
    'author': 'Vova',
    'author_email': 'vovahat09@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
