# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autohooks', 'autohooks.plugins.insert_license']

package_data = \
{'': ['*']}

install_requires = \
['autohooks>=21.7.0,<22.0.0']

setup_kwargs = {
    'name': 'autohooks-plugin-insert-license',
    'version': '0.1.3',
    'description': 'An autohooks plugin to insert license in files with insert_license',
    'long_description': None,
    'author': 'Vincent Texier',
    'author_email': 'vit@free.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
