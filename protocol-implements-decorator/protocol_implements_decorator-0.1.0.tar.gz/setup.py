# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protocol_implements_decorator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'protocol-implements-decorator',
    'version': '0.1.0',
    'description': "Adds '@implements' decorator to aid in explicit use of protocols.",
    'long_description': None,
    'author': 'rbroderi',
    'author_email': 'richard@sanguinesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
