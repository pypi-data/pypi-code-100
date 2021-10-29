# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lbpackages', 'lbpackages.classes', 'lbpackages.createdb']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0']

setup_kwargs = {
    'name': 'lbpackages',
    'version': '0.1.0',
    'description': 'Implements classes for stocks model and db client',
    'long_description': None,
    'author': 'Lionel Barbagallo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
