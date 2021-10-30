# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacedreppy', 'spacedreppy.schedulers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spacedreppy',
    'version': '0.1.0',
    'description': 'A spaced repetition Python library.',
    'long_description': '# SpacedRepPy\n',
    'author': 'Louis Schlessinger',
    'author_email': '2996982+lschlessinger1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
