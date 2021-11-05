# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaos_filler', 'chaos_filler.src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['chaos_filler = chaos_filler.main:main']}

setup_kwargs = {
    'name': 'chaos-filler',
    'version': '0.1.2',
    'description': 'chaos filler',
    'long_description': None,
    'author': 'chaos team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
