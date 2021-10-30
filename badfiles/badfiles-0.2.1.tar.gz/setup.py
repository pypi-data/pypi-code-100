# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['badfiles', 'tests']

package_data = \
{'': ['*'], 'tests': ['payloads/*']}

install_requires = \
['python-magic>=0.4.24,<0.5.0', 'yara-python>=4.1.2,<5.0.0']

extras_require = \
{':extra == "doc"': ['mkdocstrings>=0.16.1,<0.17.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocs-autorefs==0.1.1'],
 'gui': ['Gooey>=1.0.8,<2.0.0'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['badfiles = badfiles.cli:main']}

setup_kwargs = {
    'name': 'badfiles',
    'version': '0.2.1',
    'description': 'A malicious file detection engine written with Python and Yara.',
    'long_description': '# badfiles\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/badfiles">\n    <img src="https://img.shields.io/pypi/v/badfiles.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/jeffallan/badfiles/actions">\n    <img src="https://github.com/jeffallan/badfiles/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://badfiles.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/badfiles/badge/?version=latest" alt="Documentation Status">\n</a>\n\n<a href="https://pyup.io/repos/github/jeffallan/badfiles/">\n<img src="https://pyup.io/repos/github/jeffallan/badfiles/shield.svg" alt="Updates">\n</a>\n\n</p>\n\n\nA malicious file detection engine written with Python and Yara.\n\n\n* Free software: Apache-2.0\n* Documentation: <https://badfiles.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Maverick Coders',
    'author_email': 'maverickcoders@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffallan/badfiles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
