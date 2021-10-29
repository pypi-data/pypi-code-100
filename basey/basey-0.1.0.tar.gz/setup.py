# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basey',
    'version': '0.1.0',
    'description': 'Python package for encoding/decoding base 10',
    'long_description': None,
    'author': 'Dan Scott',
    'author_email': 'dscott304@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
