# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_org_tree']
install_requires = \
['anytree>=2.8.0,<3.0.0',
 'boto-collator-client>=0.1.1,<0.2.0',
 'boto3>=1.18.50,<2.0.0',
 'logdecorator>=2.2,<3.0']

entry_points = \
{'console_scripts': ['aws-org-tree = aws_org_tree:main']}

setup_kwargs = {
    'name': 'aws-org-tree',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Iain Samuel McLean Elder',
    'author_email': 'iain@isme.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
