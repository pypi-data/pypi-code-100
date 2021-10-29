# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptbmodels']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'sqlmodel>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'ptbmodels',
    'version': '0.2.14',
    'description': 'SQLModel common code for Pop the Bubble',
    'long_description': None,
    'author': 'Raaid',
    'author_email': 'raaid@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
