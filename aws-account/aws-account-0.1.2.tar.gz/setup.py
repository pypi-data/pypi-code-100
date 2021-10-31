# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_account']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'click', 'colorama']

entry_points = \
{'console_scripts': ['aws-account = aws_account.cli:main']}

setup_kwargs = {
    'name': 'aws-account',
    'version': '0.1.2',
    'description': 'Print out AWS account and identity information to verify which account/organization is currently in use.',
    'long_description': None,
    'author': 'M. Rollwagen',
    'author_email': 'rollwagen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rollwagen/aws-account',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
