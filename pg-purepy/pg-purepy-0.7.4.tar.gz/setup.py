# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pg_purepy', 'pg_purepy.conversion']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.1.0,<4.0.0',
 'arrow>=1.1.1,<2.0.0',
 'attrs>=21.2.0,<22.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'scramp>=1.4.0,<2.0.0']

extras_require = \
{':python_version < "3.10"': ['async_generator>=1.10,<2.0'],
 'docs': ['Sphinx>=3.0,<4.0',
          'sphinxcontrib-trio>=1.1.2,<2.0.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'sphinx-inline-tabs>=2021.4.11-beta.9,<2022.0.0']}

setup_kwargs = {
    'name': 'pg-purepy',
    'version': '0.7.4',
    'description': 'A pure-Python anyio-based PostgreSQL adapter.',
    'long_description': 'pg-purepy\n=========\n\n.. image:: https://img.shields.io/pypi/pyversions/pg-purepy?style=flat-square\n    :alt: PyPI - Python Version\n\npg-purepy is a pure-Python PostgreSQL wrapper based on the `anyio`_ library.\n\nA lot of this library was inspired by the `pg8000`_ library. Credits to that.\n\nRead the docs at https://pg.py.veriny.tf/.\n\n.. _anyio: https://github.com/agronholm/anyio\n.. _pg8000: https://github.com/tlocke/pg8000',
    'author': 'Lura Skye',
    'author_email': 'l@veriny.tf',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
