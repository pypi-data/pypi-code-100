# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['superprikol']
setup_kwargs = {
    'name': 'superprikol',
    'version': '1.1',
    'description': 'Prikol rzhaka klass',
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
