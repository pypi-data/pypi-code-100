# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wgop_filler', 'wgop_filler.src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wgop_filler = wgop_filler.main:main']}

setup_kwargs = {
    'name': 'wgop-filler',
    'version': '0.1.20',
    'description': '42filler',
    'long_description': None,
    'author': 'wgop team',
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
