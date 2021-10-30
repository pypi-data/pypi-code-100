# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SibylSystem', 'SibylSystem.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'sibylsystem',
    'version': '0.0.3',
    'description': 'Python Wrapper for the Sibyl System Antispam API for telegram',
    'long_description': '# SibylSystem-Py\n\n>Python3 wrapper for the Sibyl System antispam API for telegram\n\n## Installation\n\n```\npip install sibylsystem\n```\n\n# Usage\n\n```\n>>> from sibylsystem import SibylClient\n>>> a = SibylClient(host="hosturl", token="your token")\n>>> a.get_info(895373440)\n```\n',
    'author': 'Sayan Biswas',
    'author_email': 'sayan@pokurt.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AnimeKaizoku/SibylSystem-Py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
