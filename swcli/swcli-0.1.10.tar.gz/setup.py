# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swcli']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.5.7,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'httpx>=0.20.0,<0.21.0',
 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['swcli = swcli.swcli:main']}

setup_kwargs = {
    'name': 'swcli',
    'version': '0.1.10',
    'description': 'A simple CLI to do queries in StarWars API.',
    'long_description': None,
    'author': 'Pery Lemke',
    'author_email': 'pery.lemke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
