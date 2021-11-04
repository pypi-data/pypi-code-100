# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['os2datasynth']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'os2datasynth',
    'version': '0.0.1',
    'description': 'A package to generate synthethic files and sources, incoming+norsker-final-project-synthethic-data-source-498-issue-@git.magenta.dk',
    'long_description': None,
    'author': 'Norsker',
    'author_email': 'egn@magenta-aps.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
