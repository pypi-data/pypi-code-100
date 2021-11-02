# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymesis']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymesis',
    'version': '0.2.0',
    'description': 'Memoization decorator for Python, with optional TTL',
    'long_description': None,
    'author': 'Daniel Hjertholm',
    'author_email': 'daniel.hjertholm@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
