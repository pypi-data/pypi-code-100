# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hexea']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hexea',
    'version': '0.1.0.dev0',
    'description': 'Python library for the games of Hex and Y',
    'long_description': 'This is a simple library for working with the closely related connection games of Y and Hex.  This is not meant to be a standalone, playable game, but rather a set of tools one could use to implement such a game, train a machine learning model to play a game, and so forth.\n',
    'author': 'Chip Hollingsworth',
    'author_email': 'cholling@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.cholling.com/cholling/hexea',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
