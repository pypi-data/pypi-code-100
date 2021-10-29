# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hellobiswatest']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0',
 'mypy>=0.910,<0.911',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'hellobiswatest',
    'version': '0.1.0',
    'description': 'a pypi package for testing purposes by biswaroop1547',
    'long_description': None,
    'author': 'Biswaroop Bhattacharjee',
    'author_email': 'biswaroop08@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
