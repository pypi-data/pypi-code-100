# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextcore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nextcore',
    'version': '1.0.1',
    'description': 'Common components for Nextcord core libraries',
    'long_description': '# nextcore\n\nCommon components for Nextcord core libraries.\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nextcord/nextcore',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
