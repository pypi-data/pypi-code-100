# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_telegram_bot_django_persistence',
 'python_telegram_bot_django_persistence.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1', 'python-telegram-bot>=13.7']

setup_kwargs = {
    'name': 'python-telegram-bot-django-persistence',
    'version': '0.1.7',
    'description': 'Package to use Django ORM as persistence engine in Python Telegram Bot',
    'long_description': '# python-telegram-bot-django-persistence\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/python-telegram-bot-django-persistence?style=flat-square)](https://pypi.org/project/python-telegram-bot-django-persistence/)\n[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)\n\nDo you use [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) with Django\nand want persistence without additional infrastructure? We\'ve got you covered!\n\n## Quickstart\n\n### 📥 Install package\nIf you are using [poetry](https://python-poetry.org) (and if not, please, consider using it 😉):\n```shell\npoetry add python-telegram-bot-django-persistence\n```\n\nElif you are using `pip`, then just enter:\n```shell\npip install python-telegram-bot-django-persistence\n```\n\n### 🔌 Add the app to your Django project\nThen add `python_telegram_bot_django_persistence` into your `INSTALLED_APPS` in your settings file, like so:\n\n```python\nINSTALLED_APPS = [\n    ...\n    "python_telegram_bot_django_persistence",\n]\n```\n\n### ☢ Migrate your database\n```shell\npython manage migrate\n```\n\n### 🌟 Awesome! Use DjangoPersistence in python-telegram-bot\n```python\nupdater = Updater(bot=bot, use_context=True, persistence=DjangoPersistence())\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://shishenko.com"><img src="https://avatars.githubusercontent.com/u/837953?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alexander Shishenko</b></sub></a><br /><a href="https://github.com/GamePad64/python-telegram-bot-django-persistence/commits?author=GamePad64" title="Code">💻</a> <a href="https://github.com/GamePad64/python-telegram-bot-django-persistence/commits?author=GamePad64" title="Documentation">📖</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!',
    'author': 'Alexander Shishenko',
    'author_email': 'alex@shishenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GamePad64/python-telegram-bot-django-persistence',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
