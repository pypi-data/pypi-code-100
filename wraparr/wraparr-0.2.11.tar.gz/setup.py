# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wraparr']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'wraparr',
    'version': '0.2.11',
    'description': 'API wrapper for Radarr/Sonarr',
    'long_description': None,
    'author': 'muqshots',
    'author_email': '82030029+muqshots@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/muqshots/wraparr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
