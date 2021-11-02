# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline', 'pipeline.model', 'pipeline.schemas']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.10b0,<22.0',
 'dill>=0.3.4,<0.4.0',
 'pydantic>=1.8.2,<2.0.0',
 'transformers>=4.12.2,<5.0.0']

setup_kwargs = {
    'name': 'pipeline-ai',
    'version': '0.0.6',
    'description': 'Yay ml pipelines',
    'long_description': None,
    'author': 'Paul Hetherington',
    'author_email': 'paul@getneuro.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
