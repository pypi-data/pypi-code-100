# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoalchemy', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0', 'fire==0.4.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['auto-alchemy = auto-alchemy.cli:main']}

setup_kwargs = {
    'name': 'auto-alchemy',
    'version': '0.1.0',
    'description': 'Auto Alchemy is a small library container a decorator to automate initialization of variables with SQLAlchemy.',
    'long_description': '# AutoAlchemy\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/auto-alchemy">\n    <img src="https://img.shields.io/pypi/v/auto-alchemy.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/hay-kot/auto-alchemy/actions">\n    <img src="https://github.com/hay-kot/auto-alchemy/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://auto-alchemy.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/auto-alchemy/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nAuto Alchemy is a small library container a decorator to automate initialization of variables with SQLAlchemy\n\n\n* Free software: MIT\n* Documentation: <https://auto-alchemy.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Hayden Kotelman',
    'author_email': 'hay-kot@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hay-kot/auto-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
