# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcphelpers',
 'gcphelpers.prometheus',
 'gcphelpers.secretmanager',
 'gcphelpers.slack',
 'gcphelpers.storage']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-secret-manager>=2.7.2,<3.0.0',
 'google-cloud-storage>=1.42.3,<2.0.0',
 'pre-commit>=2.15.0,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'slack-sdk>=3.11.2,<4.0.0']

setup_kwargs = {
    'name': 'gcphelpers',
    'version': '0.0.11',
    'description': 'Helpers for GCP functions',
    'long_description': None,
    'author': 'Alex Orfanos',
    'author_email': 'alexandros@mailerlite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
