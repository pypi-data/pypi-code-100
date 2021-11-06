# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkm_test_project']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pkm-test-project',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'bennyl',
    'author_email': 'bennyl@voyagerlabs.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
