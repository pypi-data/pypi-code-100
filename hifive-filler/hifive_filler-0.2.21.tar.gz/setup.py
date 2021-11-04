# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hifive_filler']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hifive_filler = hifive_filler.main:main']}

setup_kwargs = {
    'name': 'hifive-filler',
    'version': '0.2.21',
    'description': '',
    'long_description': None,
    'author': 'yusata',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
