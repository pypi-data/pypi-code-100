# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redicrypt']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redicrypt-py',
    'version': '0.3.1',
    'description': 'A python library for redicrypt',
    'long_description': None,
    'author': 'Chayim Kirshen',
    'author_email': 'c@kirshen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
