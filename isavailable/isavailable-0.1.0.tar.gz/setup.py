# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isavailable']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['isavailable = isavailable:main']}

setup_kwargs = {
    'name': 'isavailable',
    'version': '0.1.0',
    'description': 'Check Python package distribution name availability on PyPI',
    'long_description': None,
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
