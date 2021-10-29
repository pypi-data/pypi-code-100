# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soset']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'soset',
    'version': '0.1.1',
    'description': 'Store and manage a collection of sets',
    'long_description': None,
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
