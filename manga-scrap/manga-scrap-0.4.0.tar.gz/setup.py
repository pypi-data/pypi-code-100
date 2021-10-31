# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manga_scrap', 'manga_scrap.proveedores']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'manga-scrap',
    'version': '0.4.0',
    'description': 'A flexible and extensible library to scrap manga and convert it to usable models',
    'long_description': None,
    'author': 'Andrés Riquelme',
    'author_email': 'andresfranco.rs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
