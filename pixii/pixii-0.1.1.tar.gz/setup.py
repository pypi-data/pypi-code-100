# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pixii']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4', 'botocore>=1.22.7,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pixii',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Pixii\n\n![PyPI - Status](https://img.shields.io/pypi/status/pixii) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pixii) ![PyPI](https://img.shields.io/pypi/v/pixii) [![GitHub license](https://img.shields.io/github/license/k2bd/pixii)](https://github.com/k2bd/pixii/blob/main/LICENSE)\n\n[![CI](https://github.com/k2bd/pixii/actions/workflows/ci.yml/badge.svg)](https://github.com/k2bd/pixii/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/k2bd/pixii/branch/main/graph/badge.svg?token=YEZCDAA1JZ)](https://codecov.io/gh/k2bd/pixii)\n',
    'author': 'Kevin Duff',
    'author_email': 'kevinkelduff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/k2bd/pixii',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
