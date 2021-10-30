# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['infpath']
setup_kwargs = {
    'name': 'infpath',
    'version': '1.2.0',
    'description': "infpath('PATH', 'OPTION') - For Using.",
    'long_description': None,
    'author': 'adamsonScripts',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
