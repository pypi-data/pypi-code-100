# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skaha', 'skaha.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'requests>=2.26.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'validators>=0.18.2,<0.19.0',
 'vos>=3.3.4,<4.0.0']

extras_require = \
{'docs': ['mkdocs-material>=7.3.6,<8.0.0', 'mkdocstrings>=0.16.2,<0.17.0']}

setup_kwargs = {
    'name': 'skaha',
    'version': '0.3.0',
    'description': 'Python Client for Skaha Container Platform in CANFAR',
    'long_description': None,
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
