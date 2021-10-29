# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaticos']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['gaticos = gaticos.main:cli']}

setup_kwargs = {
    'name': 'gaticos',
    'version': '0.5.0',
    'description': 'Librería de ejemplo',
    'long_description': '# Gaticos\n\nGaticos ("Little Cats"? "Cutey Cats"?) it\'s a simple package to print "miau" in your console or print an ascii\ndraw of a cat in your shell with quotes ¯\\_(ツ)_/¯\n\n```shell\npip install gaticos\n```\n\nPrint miaus:\n\n```shell\ngaticos -c 2\n>> Miau!\n>> Miau!\n```\n\nPrint motivation frase in spanish:\n\n```shell\ngaticos animame\nMiau!\n\n      ██            ██               A llorar a la llorería         \n    ██░░██        ██░░██                      \n    ██░░▒▒████████▒▒░░██                ████  \n  ██▒▒░░░░▒▒▒▒░░▒▒░░░░▒▒██            ██░░░░██\n  ██░░░░░░░░░░░░░░░░░░░░██            ██  ░░██\n██▒▒░░░░░░░░░░░░░░░░░░░░▒▒████████      ██▒▒██\n██░░  ██  ░░██░░  ██  ░░  ▒▒  ▒▒  ██    ██░░██\n██░░░░░░░░██░░██░░░░░░░░░░▒▒░░▒▒░░░░██████▒▒██\n██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  \n██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  \n██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    \n██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    \n██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    \n██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██    \n  ██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██      \n    ██▒▒░░▒▒▒▒░░▒▒░░░░░░▒▒░░▒▒▒▒░░▒▒██        \n      ██░░████░░██████████░░████░░██          \n      ██▓▓░░  ▓▓██░░  ░░██▓▓  ░░▓▓██                         \n```',
    'author': 'avara1986',
    'author_email': 'a.vara.1986@gmail.com',
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
