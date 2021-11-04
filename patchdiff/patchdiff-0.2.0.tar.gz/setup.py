# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patchdiff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'patchdiff',
    'version': '0.2.0',
    'description': 'MIT',
    'long_description': '[![PyPI version](https://badge.fury.io/py/patchdiff.svg)](https://badge.fury.io/py/patchdiff)\n[![CI status](https://github.com/Korijn/patchdiff/workflows/CI/badge.svg)](https://github.com/Korijn/patchdiff/actions)\n\n# Patchdiff 🔍\n',
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Korijn/patchdiff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
