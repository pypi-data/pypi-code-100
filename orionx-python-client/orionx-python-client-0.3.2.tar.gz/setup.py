# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orionx_python_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.1,<4.0.0', 'python-dotenv>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'orionx-python-client',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'adolfrodeno',
    'author_email': 'amvillalobos@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
