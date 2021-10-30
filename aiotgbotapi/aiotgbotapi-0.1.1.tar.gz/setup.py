# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotgbotapi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0,<0.71.0',
 'httpx[http2]>=0.20.0,<0.21.0',
 'pydantic>=1.8.2,<2.0.0',
 'ujson>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'aiotgbotapi',
    'version': '0.1.1',
    'description': 'Asynchronous Telegram BOT API Client',
    'long_description': '# aiotgbotapi - Asynchronous Telegram BOT API Client\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/aiotgbotapi.svg)](https://pypi.python.org/pypi/aiotgbotapi/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiotgbotapi.svg)](https://pypi.python.org/pypi/aiotgbotapi/)\n[![PyPI license](https://img.shields.io/pypi/l/aiotgbotapi.svg)](https://pypi.python.org/pypi/aiotgbotapi/)\n\n## Installation\n\n### PyPI\n\n```shell\npip install aiotgbotapi\n```\n\nor if you use [Poetry](https://python-poetry.org)\n\n```shell\npoetry add aiotgbotapi\n```\n\n## Examples\n\n### Basic example\n\n```python\nimport asyncio\nimport logging\n\nfrom aiotgbotapi import Bot\nfrom aiotgbotapi.filters import Filters\nfrom aiotgbotapi.types import Message\n\nbot = Bot("BOT TOKEN HERE")\n\n\n@bot.on_message(filters=Filters.command(\'start\'))\nasync def on_start_command(_bot: Bot, message: Message):\n    await message.reply(f"Hello, {message.from_.mention}")\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    asyncio.run(bot.run())\n\n```',
    'author': 'Pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylakey/aiotgbotapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
