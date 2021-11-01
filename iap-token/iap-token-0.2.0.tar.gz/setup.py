# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iap_token']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iap-token',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Myung Kim',
    'author_email': 'agilemlops@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
