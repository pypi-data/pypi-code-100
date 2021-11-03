# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['diglett']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0',
 'ipython>=7.26.0,<8.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy==1.19.5',
 'pandas==1.3.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'diglett',
    'version': '0.2.0',
    'description': 'Tools for data wrangling.',
    'long_description': '# Diglett\n\n[![Tests](https://github.com/asdfgeoff/diglett/workflows/Tests/badge.svg)](https://github.com/asdfgeoff/diglett/actions?workflow=Tests) [![Codecov](https://codecov.io/gh/asdfgeoff/diglett/branch/master/graph/badge.svg)](https://codecov.io/gh/asdfgeoff/diglett) [![PyPI](https://img.shields.io/pypi/v/diglett.svg)](https://pypi.org/project/diglett/) [![Read the Docs](https://readthedocs.org/projects/diglett/badge/)](https://diglett.readthedocs.io/)\n\n## What it does\n\nDiglett is a collection of my most frequently used and reusable functions for data analysis, data wrangling, and machine learning. I have largely packaged them together for my own benefit, but I hope you will find something useful in here for yourself.\n\n\n![Image of Diglett pokemon](diglett.png)\n\n\n## Installing\n\nTo install the most recently published version from PyPI:\n```\npip install diglett\n```\n\nTo install a (possibly more recent, but less polished) version: clone this repo and run:\n```\npip install -e .\n```',
    'author': 'Geoff Ruddock',
    'author_email': 'geoff@ruddock.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
