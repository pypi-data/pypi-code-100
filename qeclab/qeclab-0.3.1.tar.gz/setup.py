# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qeclab']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.4,<0.4.0',
 'multiprocess>=0.70.12,<0.71.0',
 'pandas>=1.3.0,<2.0.0',
 'qecstruct>=0.2.6,<0.3.0']

setup_kwargs = {
    'name': 'qeclab',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'maxtremblay',
    'author_email': 'm@xtremblay.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
