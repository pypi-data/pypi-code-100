# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spellbot',
 'spellbot.cogs',
 'spellbot.interactions',
 'spellbot.migrations',
 'spellbot.migrations.versions',
 'spellbot.models',
 'spellbot.services',
 'spellbot.web',
 'spellbot.web.api']

package_data = \
{'': ['*'], 'spellbot.web': ['templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.37.9,<0.38.0',
 'SQLAlchemy>=1.4.26,<2.0.0',
 'aiohttp-jinja2>=1.5,<2.0',
 'aiohttp-retry>=2.4.6,<3.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'alembic>=1.7.4,<2.0.0',
 'asgiref>=3.4.1,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'discord-py-interactions>=3.0.2,<4.0.0',
 'discord.py==1.7.3',
 'dunamai>=1.7.0,<2.0.0',
 'expiringdict>=1.2.1,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'humanize>=3.12.0,<4.0.0',
 'hupper>=1.10.3,<2.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'pygicord>=1.0.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'pytz>=2021.3,<2022.0',
 'supervisor>=4.2.2,<5.0.0',
 'types-PyYAML>=6.0.0,<7.0.0',
 'types-python-dateutil>=2.8.2,<3.0.0',
 'types-pytz>=2021.3.0,<2022.0.0',
 'types-toml>=0.10.1,<0.11.0',
 'wrapt==1.13.2']

entry_points = \
{'console_scripts': ['spellbot = spellbot:main']}

setup_kwargs = {
    'name': 'spellbot',
    'version': '7.1.0',
    'description': 'The Discord bot for SpellTable',
    'long_description': '<img align="right" width="200" src="https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png" />\n\n# SpellBot\n\n[![build][build-badge]][build]\n[![uptime][uptime-badge]][uptime]\n[![metrics][metrics-badge]][metrics]\n[![pypi][pypi-badge]][pypi]\n[![codecov][codecov-badge]][codecov]\n[![CodeFactor][factor-badge]][factor]\n[![CodeQL][codeql-badge]][security]\n[![python][python-badge]][python]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n[![patreon][patreon-button]][patreon]\n[![follow][follow-badge]][follow]\n\nThe Discord bot for [SpellTable][spelltable].\n\n[![add-bot][add-bot-button]][add-bot]\n\n## 🤖 Using SpellBot\n\nJust looking to play a game of Magic? Run the command `/lfg` and SpellBot will help you out!\n\n<img src="https://user-images.githubusercontent.com/1903876/137987904-6fcdf273-5b60-4692-9389-a51d65c0a424.png" width="600" alt="/lfg" />\n\nSpellBot uses [Discord slash commands](https://discord.com/blog/slash-commands-are-here). Each command provides its own help documentation that you can view directly within Discord itself before running the command. Take a look and see what\'s available by typing `/` and browsing the commands for SpellBot!\n\n### 🎤 Feedback\n\nThoughts and suggestions? Come join us on the\n[SpellTable Discord server][discord-invite]! Please also feel free\nto [directly report any bugs][issues] that you encounter.\n\n## 🙌 Support Me\n\nI\'m keeping SpellBot running using my own money but if you like the bot and want\nto help me out, please consider [becoming a patron][patreon].\n\n## ❤️ Contributing\n\nIf you\'d like to become a part of the SpellBot development community please\nfirst know that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and\nthen see our [documentation on how to contribute](CONTRIBUTING.md) for details\non how to get started.\n\n## 🐳 Docker Support\n\nSpellBot can be run via docker. Our image is published to\n[lexicalunit/spellbot][docker-hub]. See [our documentation on Docker Support](DOCKER.md) for help\nwith installing and using it.\n\n## 🔍 Fine-print\n\nAny usage of SpellBot implies that you accept the following policies.\n\n- [Privacy Policy](PRIVACY_POLICY.md)\n- [Terms of Service](TERMS_OF_SERVICE.md)\n\n---\n\n[MIT][mit] © [amy@lexicalunit][lexicalunit] et [al][contributors]\n\n[add-bot-button]: https://user-images.githubusercontent.com/1903876/88951823-5d6c9a00-d24b-11ea-8523-d256ccbf4a3c.png\n[add-bot]: https://discordapp.com/api/oauth2/authorize?client_id=725510263251402832&permissions=2416045137&scope=applications.commands%20bot\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black]: https://github.com/psf/black\n[build-badge]: https://github.com/lexicalunit/spellbot/workflows/build/badge.svg\n[build]: https://github.com/lexicalunit/spellbot/actions\n[codecov-badge]: https://codecov.io/gh/lexicalunit/spellbot/branch/master/graph/badge.svg\n[codecov]: https://codecov.io/gh/lexicalunit/spellbot\n[codeql-badge]: https://github.com/lexicalunit/spellbot/workflows/CodeQL/badge.svg\n[contributors]: https://github.com/lexicalunit/spellbot/graphs/contributors\n[discord-invite]: https://discord.gg/zXzgqMN\n[docker-hub]: https://hub.docker.com/r/lexicalunit/spellbot\n[factor-badge]: https://www.codefactor.io/repository/github/lexicalunit/spellbot/badge\n[factor]: https://www.codefactor.io/repository/github/lexicalunit/spellbot\n[follow-badge]: https://img.shields.io/twitter/follow/SpellBotIO?style=social\n[follow]: https://twitter.com/intent/follow?screen_name=SpellBotIO\n[issues]: https://github.com/lexicalunit/spellbot/issues\n[patreon]: https://www.patreon.com/lexicalunit\n[patreon-button]: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Dlexicalunit%26type%3Dpatrons88951826-5e053080-d24b-11ea-9a81-f1b5431a5d4b.png\n[lexicalunit]: http://github.com/lexicalunit\n[metrics-badge]: https://img.shields.io/badge/metrics-grafana-orange.svg\n[metrics]: https://lexicalunit.grafana.net/d/4TSUCbcMz/spellbot?orgId=1\n[mit-badge]: https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://img.shields.io/pypi/v/spellbot\n[pypi]: https://pypi.org/project/spellbot/\n[python-badge]: https://img.shields.io/badge/python-3.8+-blue.svg\n[python]: https://www.python.org/\n[security]: https://github.com/lexicalunit/spellbot/security\n[spelltable]: https://spelltable.wizards.com/\n[uptime-badge]: https://img.shields.io/uptimerobot/ratio/m785764282-c51c742e56a87d802968efcc\n[uptime]: https://uptimerobot.com/dashboard#785764282\n',
    'author': 'Amy Troschinetz',
    'author_email': 'spellbot@lexicalunit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://spellbot.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
