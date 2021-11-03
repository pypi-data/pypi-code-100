# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastoad_notebooks',
 'fastoad_notebooks.01_tutorial',
 'fastoad_notebooks.01_tutorial.data',
 'fastoad_notebooks.01_tutorial.img',
 'fastoad_notebooks.02_CeRAS_case_study',
 'fastoad_notebooks.02_CeRAS_case_study.data',
 'fastoad_notebooks.02_CeRAS_case_study.img',
 'fastoad_notebooks.03_custom_modules',
 'fastoad_notebooks.03_custom_modules.data',
 'fastoad_notebooks.03_custom_modules.img',
 'fastoad_notebooks.03_custom_modules.modules']

package_data = \
{'': ['*']}

install_requires = \
['fast-oad>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'fast-oad-notebooks',
    'version': '0.2.0',
    'description': 'Tutorial notebooks for FAST-OAD',
    'long_description': None,
    'author': 'Scott DELBECQ',
    'author_email': 'Scott.DELBECQ@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
