# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prompt2slip']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.10.0,<2.0.0',
 'torchtyping>=0.1.4,<0.2.0',
 'transformers>=4.11.3,<5.0.0']

setup_kwargs = {
    'name': 'prompt2slip',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
    'author': 'akiFQC',
    'author_email': 'yakaredori@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
