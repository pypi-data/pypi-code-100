# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pure_chacha20']
setup_kwargs = {
    'name': 'pure-chacha20',
    'version': '0.1.0',
    'description': 'a pure Python implementation of ChaCha20 and XChaCha20',
    'long_description': None,
    'author': "Jack O'Connor",
    'author_email': 'oconnor663@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oconnor663/pure_python_salsa_chacha',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
