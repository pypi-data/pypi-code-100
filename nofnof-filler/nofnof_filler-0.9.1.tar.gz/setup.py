# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nofnof_filler', 'nofnof_filler.src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nofnof-filler',
    'version': '0.9.1',
    'description': 'Assignment program using python in 42rush',
    'long_description': None,
    'author': 'kegoshi, rsato, kkamioka, omotoki',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
