# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shellfish']

package_data = \
{'': ['*']}

install_requires = \
['xtyping>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'shellfish',
    'version': '0.0.2',
    'description': 'shellfish ~ shell and file-system utils',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
