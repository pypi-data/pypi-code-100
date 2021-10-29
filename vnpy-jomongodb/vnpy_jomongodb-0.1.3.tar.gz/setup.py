# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vnpy_jomongodb']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.8.1,<5.0.0',
 'pandas>=1.3.4,<2.0.0',
 'tzlocal>=4.0.1,<5.0.0',
 'vnpy-mongodb>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'vnpy-jomongodb',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'FangyangJz',
    'author_email': 'fangyang.jing@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
