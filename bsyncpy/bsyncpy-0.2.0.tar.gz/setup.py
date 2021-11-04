# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bsyncpy']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'bsyncpy',
    'version': '0.2.0',
    'description': 'Tools to autogenerate a Python SDK for BuildingSync given an XSD',
    'long_description': None,
    'author': 'Joel Bender',
    'author_email': 'joel@carrickbender.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
