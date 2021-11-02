# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysmore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysmore',
    'version': '0.0.1',
    'description': 'Python version of SMORe: Modularize Graph Embedding for Recommendation',
    'long_description': '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Github Actions](https://github.com/josix/pysmore/actions/workflows/python-check.yaml/badge.svg)](https://github.com/josix/pysmore/wayback-machine-saver/actions/workflows/python-check.yaml)\n\n[![PyPI Package latest release](https://img.shields.io/pypi/v/pysmore.svg?style=flat-square)](https://pypi.org/project/pysmore/)\n[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/pysmore?style=flat-square)](https://pypi.org/project/pysmore/)\n[![Supported versions](https://img.shields.io/pypi/pyversions/pysmore.svg?style=flat-square)](https://pypi.org/project/pysmore/)\n\n\n# pysmore\n\nPython version of SMORe: Modularize Graph Embedding for Recommendation\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n\n## Usage\n\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nJosix Wang <josixwang@gmail.com>\n\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/1.1.2) version 1.1.2\n',
    'author': 'Josix Wang',
    'author_email': 'josixwang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/josix/pysmore',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
