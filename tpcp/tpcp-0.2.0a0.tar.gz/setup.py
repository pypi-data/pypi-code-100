# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpcp', 'tpcp._utils', 'tpcp.optimize', 'tpcp.validation']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.21.3,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'scikit-learn>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'tpcp',
    'version': '0.2.0a0',
    'description': 'Pipeline and Dataset helpers for complex algorithm evaluation.',
    'long_description': None,
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
