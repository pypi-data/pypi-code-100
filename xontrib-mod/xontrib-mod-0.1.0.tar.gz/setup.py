# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xontrib-mod',
    'version': '0.1.0',
    'description': 'Lazily access modules without importing them first.',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
