# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kak_rope']

package_data = \
{'': ['*']}

install_requires = \
['rope>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['kak-rope = kak_rope:main']}

setup_kwargs = {
    'name': 'kak-rope',
    'version': '0.3.0',
    'description': 'Python refactoring actions for kakoune',
    'long_description': '## kak-rope\n\nIntegrating [rope](https://github.com/python-rope/rope) refactoring\nlibrary with kakoune.\n\n## Installation\n\nFirst, install the `kak-rope` binary and its dependencies:\n\n```bash\npipx install kak-rope\n```\n\nThen, configure kakoune, for instance using `plug.kak`:\n\n\n```\nplug "git+https://git.sr.ht/~dmerej/kak-rope" config %{\n  # Suggested mappings\n  declare-user-mode rope\n  map global user r \' :enter-user-mode rope<ret>\' -docstring \'enter rope mode\'\n  map global rope a \':rope-add-import \' -docstring \'add import\'\n}\n```\n\n## Usage\n\nSee builtin kakoune help. All commands defined in this module starts with `rope-`.\n\n## Contributing\n\n* Install [poetry](https://python-poetry.org/)\n* Install required dependencies\n\n```\npoetry install\n```\n\nBefore submitting a change, run the following commands:\n\n```\npoetry run invoke lint\n```\n\nYou can now use [git-send-email](https://git-send-email.io/) and send a patch to  https://lists.sr.ht/~dmerej/kak-rope\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'dimitri@dmerej.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~dmerej/kak-rope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
