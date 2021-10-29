# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modelaapi']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.41.0,<2.0.0']

setup_kwargs = {
    'name': 'modelaapi',
    'version': '0.4.135',
    'description': 'data science for modela.',
    'long_description': '## What is Modela.ai API?\n\nModela.ai is an automatic machine learning platform for Kubernetes. The modela.ai api is a set\nof custom kuberentes resources in the area of data science and automatic machine learning. \nThe API is implemented by the modela.ai platform which is closed source as the moment. \n\nFor complete documentation on the modela.ai API, please visit our documentation at [www.modela.ai](https://www.modela.ai/).\n\n## Installing Modela.ai\n\nThe modela.ai platform can be installed via an helm chart. For a complete installation procedure\nplease refer to the modela.ai documentation at [www.modela.ai](https://www.modela.ai/docs).\n\n## Using Modela.ai\n\nThe Modela API specify a set of crds and services which are implemented by the modela.ai platform. ',
    'author': 'tsagi',
    'author_email': 'tsagi@metaprov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/metaprov/modela/pycode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
