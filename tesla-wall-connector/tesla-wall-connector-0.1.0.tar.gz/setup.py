# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tesla_wall_connector']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'backoff>=1.11.1,<2.0.0', 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'tesla-wall-connector',
    'version': '0.1.0',
    'description': 'API Library for communicating with a Tesla Wall Connector',
    'long_description': None,
    'author': 'Einar Bragi Hauksson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
