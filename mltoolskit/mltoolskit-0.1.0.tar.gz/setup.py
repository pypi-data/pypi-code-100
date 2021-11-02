# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mltoolskit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mltoolskit',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'MarkusSagen',
    'author_email': 'markus.john.sagen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
