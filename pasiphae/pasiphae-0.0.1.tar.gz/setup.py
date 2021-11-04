# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pasiphae']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'graphql-core>=3.1.6,<4.0.0']

setup_kwargs = {
    'name': 'pasiphae',
    'version': '0.0.1',
    'description': 'Generate and update ariadne service from graphql schema',
    'long_description': None,
    'author': 'Damian Świstowski',
    'author_email': 'damian@swistowski.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
