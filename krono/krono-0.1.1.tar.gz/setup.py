# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['krono']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['krono = krono.main:app']}

setup_kwargs = {
    'name': 'krono',
    'version': '0.1.1',
    'description': 'Aplicativo de linha de comando para rastrear o tempo de trabalho',
    'long_description': '# Rastreador de tempo\n\nRastreador de tempo com gerador de invoice\n',
    'author': 'rafaelmatsumoto',
    'author_email': 'rafael.matsumoto43@catolicasc.edu.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
