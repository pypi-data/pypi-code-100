# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_bell']

package_data = \
{'': ['*']}

install_requires = \
['12factor-configclasses>=1.0.0,<2.0.0',
 'anyio>=3.3.4,<4.0.0',
 'asyncclick>=8.0.1,<9.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'rich>=10.12.0,<11.0.0',
 'telethon>=1.23,<2.0']

entry_points = \
{'console_scripts': ['tbell = telegram_bell.bell:cli']}

setup_kwargs = {
    'name': 'telegram-bell',
    'version': '0.6.0',
    'description': 'Notify you when something is mentioned in a telegram channel',
    'long_description': "# telegram-bell\n\n![PyPI](https://img.shields.io/pypi/v/telegram-bell)\n\nNotify you when something is mentioned in a telegram channel.\n\n## Install\n\n    pip install telegram-bell\n\n## Usage\n\n### CLI\n\n#### Run\n\n    tbell run\n\nBefore you can use, it will ask you for:\n\n- your Telegram API ID\n- your Telegram API hash\n- channels and keywords which you want to get notified\n- Telegram token (2FA)\n\nThen, the app will resend you the coinciding messages to your 'Saved Messages' channel in Telegram.\n\n#### Config\n\n    tbell config\n\n#### Show susbscribed channels\n\n    tbell show\n\n### Systemd user service\n\nClone the repo and:\n\n    cd telegram-bell/scripts\n    sh install_service.sh\n    sh start_service.sh # it will ask you for config\n\nCheck the service is running:\n\n    sh check_service.sh\n\nYou can check the services logs too:\n\n    sh show_service_logs.sh\n\nIf the service fails or the machine is restarted, the service will run transparently again.\n\nIf you want to change your config in some moment:\n\n    tbell config\n    sh restart_service.sh",
    'author': 'Pablo Cabezas',
    'author_email': 'headsrooms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
