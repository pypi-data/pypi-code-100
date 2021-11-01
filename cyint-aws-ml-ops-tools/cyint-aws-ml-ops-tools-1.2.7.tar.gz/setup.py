# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyint_aws_ml_ops_tools', 'cyint_aws_ml_ops_tools.glue']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.6,<2.0.0']

setup_kwargs = {
    'name': 'cyint-aws-ml-ops-tools',
    'version': '1.2.7',
    'description': 'Tools for assisting with managing modern ml-ops-pipelines in AWS Sagemaker',
    'long_description': None,
    'author': 'Daniel Fredriksen',
    'author_email': 'dfredriksen@cyint.technology',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
