# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['continuousintegrationdependency']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'continuousintegrationdependency',
    'version': '1.0.0.4.dev0',
    'description': '',
    'long_description': None,
    'author': 'Aaron Shiels',
    'author_email': 'aaron.shiels@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
