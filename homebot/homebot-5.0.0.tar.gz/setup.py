# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homebot',
 'homebot.core',
 'homebot.lib.libadmin',
 'homebot.lib.libmdlintf',
 'homebot.lib.libupload',
 'homebot.modules.ci',
 'homebot.modules.ci.projects.aosp',
 'homebot.modules.ci.projects.lineageos-r',
 'homebot.modules.ci.projects.lineageos-s',
 'homebot.modules.ci.projects.twrpdtgen',
 'homebot.modules.core',
 'homebot.modules.lineageos_updates',
 'homebot.modules.shell',
 'homebot.modules.speedtest',
 'homebot.modules.xda']

package_data = \
{'': ['*'], 'homebot.modules.ci.projects.aosp': ['tools/*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'PyYAML>=6.0,<7.0',
 'natsort>=8.0.0,<9.0.0',
 'paramiko>=2.8.0,<3.0.0',
 'python-telegram-bot>=13.7,<14.0',
 'requests>=2.26.0,<3.0.0',
 'speedtest-cli>=2.1.3,<3.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'twrpdtgen>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'homebot',
    'version': '5.0.0',
    'description': 'A Telegram bot written in Python',
    'long_description': None,
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
