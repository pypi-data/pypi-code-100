# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transpi']

package_data = \
{'': ['*']}

install_requires = \
['requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'transpi',
    'version': '0.4.0',
    'description': 'Transpi is a translation tool',
    'long_description': None,
    'author': 'ischaojie',
    'author_email': 'zhuzhezhe95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
