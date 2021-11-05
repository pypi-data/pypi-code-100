# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_cli_run']

package_data = \
{'': ['*']}

install_requires = \
['diot>=0.1,<0.2',
 'pandas>=1.3,<2.0',
 'pardoc>=0.0.3,<0.0.4',
 'pipen-args>=0.1,<0.2',
 'pipen>=0.2,<0.3',
 'pyparam>=0.4,<0.5',
 'rich>=10.12,<11.0']

entry_points = \
{'pipen_cli': ['cli-run = pipen_cli_run:PipenCliRunPlugin']}

setup_kwargs = {
    'name': 'pipen-cli-run',
    'version': '0.1.0',
    'description': 'A pipen cli plugin to run a process or a pipeline',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
