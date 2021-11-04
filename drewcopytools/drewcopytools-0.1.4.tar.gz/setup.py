# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drewcopytools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'drewcopytools',
    'version': '0.1.4',
    'description': 'Utility code that I use in many of my python projects.',
    'long_description': None,
    'author': 'Andrew Ritz',
    'author_email': 'drew@august-harper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
