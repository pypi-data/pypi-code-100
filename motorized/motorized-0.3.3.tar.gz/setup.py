# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motorized']

package_data = \
{'': ['*']}

install_requires = \
['motor>=2.5.1,<3.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'motorized',
    'version': '0.3.3',
    'description': 'Asyncio mongodb ODM',
    'long_description': None,
    'author': 'Sebastien Nicolet',
    'author_email': 'snicolet95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
