# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.games', 'brain_games.scripts']

package_data = \
{'': ['*']}

install_requires = \
['prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-calc = brain_games.scripts.brain_calc:main',
                     'brain-even = brain_games.scripts.brain_even:main',
                     'brain-games = brain_games.scripts.brain_games:main',
                     'brain-gcd = brain_games.scripts.brain_gcd:main',
                     'brain-prime = brain_games.scripts.brain_prime:main',
                     'brain-progression = '
                     'brain_games.scripts.brain_progression:main',
                     'brain-progression1 = '
                     'brain_games.games.brain_progression:main']}

setup_kwargs = {
    'name': 'siderai-brain-games',
    'version': '1.1.0',
    'description': 'Brain Games is a pack of five console arithmetic games',
    'long_description': None,
    'author': 'Alexander Sidorov',
    'author_email': 'sidai@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/siderai/brain-games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
