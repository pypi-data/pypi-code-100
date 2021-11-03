# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'adash',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'atu4403',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
