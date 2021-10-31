# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d2b_lwc']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'd2b-lwc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joshua OLulana',
    'author_email': 'joshua.olulana@data2bots.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
