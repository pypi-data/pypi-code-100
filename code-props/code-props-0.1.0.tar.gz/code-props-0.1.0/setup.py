# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_props']

package_data = \
{'': ['*']}

install_requires = \
['tree-sitter>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'code-props',
    'version': '0.1.0',
    'description': 'Identify basic code properties such as module, method and parameter names from application source',
    'long_description': '',
    'author': 'Prabhu Subramanian',
    'author_email': 'prabhu@ngcloud.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rosa.cx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
