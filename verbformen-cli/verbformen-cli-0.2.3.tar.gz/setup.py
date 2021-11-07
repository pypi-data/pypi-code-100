# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verbformen_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.0,<8.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.7.0,<11.0.0',
 'xextract>=0.1.8,<0.2.0']

entry_points = \
{'console_scripts': ['verbformen = verbformen_cli.cli:lookup']}

setup_kwargs = {
    'name': 'verbformen-cli',
    'version': '0.2.3',
    'description': 'Verbformen CLI',
    'long_description': '## Verbformen CLI\n\nUnofficial python client for the German-English dictionary at verbformen.com. Verbformen provides detailed conjugations and declensions of German words, along with a useful summary card that includes: \n\n- verb endings,\n- noun gender,\n- noun endings,\n- adjective endings, and\n- definitions\n\n### Installation\n\n```bash\npip install verbformen-cli\n```\n\n### Usage\nFrom the terminal:\n```\n$ verbformen Wörterbuch \n           ╭────────── Wörterbuch ───────────╮\n           │ A1 • Neutral • Endings: es/ü-er │\n           │         das Wörterbuch          │\n           │  Wörterbuch(e)s • Wörterbücher  │\n           │                                 │\n           │  dictionary, lexicon, wordbook  │\n           ╰─────────────────────────────────╯\n\n$ verbformen nachschlagen\n   ╭───────────────── nachschlagen ──────────────────╮\n   │ B1 • irregular • haben (also, sein)             │\n   │                  nachschlagen                   │\n   │ schlägt nach • schlug nach • hat nachgeschlagen │\n   │                                                 │\n   │                     look up                     │\n   ╰─────────────────────────────────────────────────╯\n\n```\n\nor, in code:\n```python\nfrom verbformen_cli import Client, PartOfSpeech\n\nclient = Client.default_client()\nclient.search("essen")\n# {\n#   "search": "essen",\n#   "definitions": [\n#     "eat",\n#     "consume"\n#   ],\n#   "part_of_speech": "verb",\n#   "text": "essen",\n#   "behavior": "irregular",\n#   "present": "isst",\n#   "imperfect": "aß",\n#   "perfect": "hat gegessen",\n#   "auxiliary_verb": "haben",\n#   "flection": "Active",\n#   "use": "Main",\n#   "level": "A1"\n# }\n```\n',
    'author': 'Nicholas Miller',
    'author_email': 'njmiller6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/millern/verbformen-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
