# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['terramagic']
install_requires = \
['click>=8.0.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pyfiglet>=0.8.post1,<0.9',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['terramagic = terramagic:main']}

setup_kwargs = {
    'name': 'terramagic',
    'version': '0.1.1',
    'description': 'A automate tool for terraform projects',
    'long_description': "# Terramagic CLI\n\n\n## Motivation\n\nEvery time , I needed create a terraform files to a new project, and a new terraform files., but this is not good. and now we have a Terramagic tool to help us to create a terraform files.\n\n## Requirements\n\n- Python 3.9 >=\n\n## How to install?\n\n```shell\npip install terramagic\n```\n\n## Hands on\n\n[![asciicast](https://asciinema.org/a/xeSFySIjxwGK4x4m83y8BfbZY.png)](https://asciinema.org/a/xeSFySIjxwGK4x4m83y8BfbZY)\n\n## Check the version\n\n```shell\nterramagic --version\n\n _____                   __  __             _      \n|_   _|__ _ __ _ __ __ _|  \\/  | __ _  __ _(_) ___ \n  | |/ _ \\ '__| '__/ _` | |\\/| |/ _` |/ _` | |/ __|\n  | |  __/ |  | | | (_| | |  | | (_| | (_| | | (__ \n  |_|\\___|_|  |_|  \\__,_|_|  |_|\\__,_|\\__, |_|\\___|\n                                      |___/        \n\n\nTerraMagic is a tool for creating a structure of folders and files for Terraform\nAuthor: https://github.com/miltlima\nVersion: 0.0.9\n```\n\n## Usage(Ex.)\n\n```shell\nterramagic create-project --name=<project_name> --env=<env>\n```\n\n```shell\nterramagic create-project --name=terraform --env=prod --env=dev\n```\n\n## How to use this tool ?\n\n```shell\nUsage: terramagic create-project [OPTIONS]\n\n\nOptions:\n  -n, --name TEXT  Name of the project\n  -e, --env TEXT   Environment name(dev, test, prd)\n  --help           Show this message and exit.\n```\n\nEnjoy!\n",
    'author': 'Milton Jesus',
    'author_email': 'milton.lima@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miltlima/terramagic',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
