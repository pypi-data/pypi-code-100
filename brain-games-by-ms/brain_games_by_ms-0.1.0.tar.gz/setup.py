# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.games', 'brain_games.scripts']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-calc = brain_games.scripts.brain_calc:main',
                     'brain-even = brain_games.scripts.brain_even:main',
                     'brain-games = brain_games.scripts.brain_games:main',
                     'brain-gcd = brain_games.scripts.brain_gcd:main',
                     'brain-is-prime = brain_games.scripts.brain_is_prime:main',
                     'brain-progression = '
                     'brain_games.scripts.brain_progression:main']}

setup_kwargs = {
    'name': 'brain-games-by-ms',
    'version': '0.1.0',
    'description': 'Brain-games, project on hexlet',
    'long_description': None,
    'author': 'Mikhail Smotrin',
    'author_email': 'iseeuqq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mickysmt/python-project-lvl1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
