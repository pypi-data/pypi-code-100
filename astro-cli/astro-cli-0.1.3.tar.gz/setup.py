# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astro', 'astro.cmd']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'dateparser>=1.1.0,<2.0.0',
 'diskcache>=5.2.1,<6.0.0',
 'skyfield>=1.39,<2.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['astro = astro.cli:cli']}

setup_kwargs = {
    'name': 'astro-cli',
    'version': '0.1.3',
    'description': 'query astronomical events from the CLI',
    'long_description': None,
    'author': 'redraw',
    'author_email': 'redraw@sdf.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
