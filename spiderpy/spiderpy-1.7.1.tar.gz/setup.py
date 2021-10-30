# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spiderpy', 'spiderpy.devices']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'spiderpy',
    'version': '1.7.1',
    'description': 'Python wrapper for the Spider API, a way to manage your Spider installation',
    'long_description': None,
    'author': 'Peter Nijssen',
    'author_email': 'peter@peternijssen.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
