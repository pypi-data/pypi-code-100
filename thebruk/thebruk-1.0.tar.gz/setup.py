# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['thebruk']
setup_kwargs = {
    'name': 'thebruk',
    'version': '1.0',
    'description': 'Test test',
    'long_description': None,
    'author': 'TheBruk',
    'author_email': 'no.point2007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
