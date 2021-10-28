# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torrent_organizer', 'torrent_organizer.console']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'parse-torrent-title>=2.3,<3.0',
 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['torrent_organizer = torrent_organizer.console.run:cli']}

setup_kwargs = {
    'name': 'torrent-organizer',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Juan Olvera',
    'author_email': 'juan@jolvera.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j0lv3r4/torrent-organizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
