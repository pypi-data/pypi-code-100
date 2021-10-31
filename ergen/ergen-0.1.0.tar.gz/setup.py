# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ergen']

package_data = \
{'': ['*'], 'ergen': ['template/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'pydantic>=1.8.2,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ergen = ergen.cli:app']}

setup_kwargs = {
    'name': 'ergen',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Naoya Yamashita',
    'author_email': 'conao3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
