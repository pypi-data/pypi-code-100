# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enact']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enact',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Ivan Dmitriesvky',
    'author_email': 'ivan.dmitrievsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
