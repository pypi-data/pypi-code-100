# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcentral']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'bcentral',
    'version': '0.1.0',
    'description': 'Chilean Central Bank API Client',
    'long_description': None,
    'author': 'Héctor Urbina',
    'author_email': 'hurbinas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
