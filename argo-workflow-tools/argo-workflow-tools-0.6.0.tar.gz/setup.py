# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argo_workflow_tools', 'argo_workflow_tools.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'requests>=2.26.0,<3.0.0',
 'urllib3>=1.26.7,<2.0.0']

setup_kwargs = {
    'name': 'argo-workflow-tools',
    'version': '0.6.0',
    'description': 'A suite of tools to ease ML pipeline development with Argo Workflows',
    'long_description': None,
    'author': 'Diagnostic Robotics',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DiagnosticRobotics/argo-workflow-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
