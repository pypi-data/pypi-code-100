# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agency']

package_data = \
{'': ['*']}

install_requires = \
['enumb>=0.1.2,<0.2.0', 'parse>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'agency',
    'version': '0.1.1',
    'description': 'User Agent parsing and creation',
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
