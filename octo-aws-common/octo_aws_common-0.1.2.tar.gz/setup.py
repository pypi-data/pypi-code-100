# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octo_aws_common']

package_data = \
{'': ['*']}

install_requires = \
['aws-lambda-powertools>=1.21.1,<2.0.0', 'boto3>=1.19.7,<2.0.0']

setup_kwargs = {
    'name': 'octo-aws-common',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
