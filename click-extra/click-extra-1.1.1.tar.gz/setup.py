# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_extra', 'click_extra.tests']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=21.0.0,<22.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=8.0.2,<9.0.0',
 'cloup>=0.12.1,<0.13.0',
 'tomli>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'click-extra',
    'version': '1.1.1',
    'description': '🌈 Extra colorization and configuration file for Click.',
    'long_description': '# Click Extra\n\n[![Last release](https://img.shields.io/pypi/v/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Python versions](https://img.shields.io/pypi/pyversions/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Unittests status](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml?query=branch%3Amain)\n[![Coverage status](https://codecov.io/gh/kdeldycke/click-extra/branch/main/graph/badge.svg)](https://codecov.io/gh/kdeldycke/click-extra/branch/main)\n\n**What is Click Extra?**\n\n`click-extra` is a collection of helpers and utilities for\n[Click](https://click.palletsprojects.com), the Python CLI framework.\n\nIt provides boilerplate code and good defaults, as weel as some workarounds\nand patches that have not reached upstream yet (or are unlikely to).\n\n## Used in\n\n- [Meta Package Manager](https://github.com/kdeldycke/meta-package-manager#readme) - A unifying CLI for multiple package managers.\n- [Mail Deduplicate](https://github.com/kdeldycke/mail-deduplicate#readme) - A CLI to deduplicate similar emails.\n\n## Installation\n\nInstall `click-extra` with `pip`:\n\n```shell-session\n$ pip install click-extra\n```\n\n## Features\n\n- TOML configuration file loader\n- Colorization of help screens\n- ``--color/--no-color`` option flag\n- Colored ``--version`` option\n- Colored ``--verbosity`` option and logs\n- ``--time/--no-time`` flag to measure duration of command execution\n- Platform recognition utilities\n- New conditional markers for `pytest`:\n    - `@skip_linux`, `@skip_macos` and `@skip_windows`\n    - `@unless_linux`, `@unless_macos` and `@unless_windows`\n    - `@destructive` and `@non_destructive`\n\n### TOML configuration file\n\nAllows a CLI to read defaults options from a configuration file.\n\nHere is a sample:\n\n``` toml\n# My default configuration file.\n\n[my_cli]\nverbosity = "DEBUG"\nmanager = ["brew", "cask"]\n\n[my_cli.search]\nexact = true\n```\n\n### Colorization of help screen\n\nExtend [Cloup\'s own help formatter and theme](https://cloup.readthedocs.io/en/stable/pages/formatting.html#help-formatting-and-themes) to add colorization of:\n- Options\n- Choices\n- Metavars\n\nThis has been discussed upstream at:\n- https://github.com/janluke/cloup/issues/97\n- https://github.com/click-contrib/click-help-colors/issues/17\n- https://github.com/janluke/cloup/issues/95\n\n## Dependencies\n\nHere is a graph of Python package dependencies:\n\n![click-extra dependency graph](https://github.com/kdeldycke/click-extra/raw/main/dependencies.png)\n\n## Development\n\n[Development guidelines](https://kdeldycke.github.io/meta-package-manager/development.html)\nare the same as\n[parent project `mpm`](https://github.com/kdeldycke/meta-package-manager), from\nwhich `click-extra` originated.\n',
    'author': 'Kevin Deldycke',
    'author_email': 'kevin@deldycke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kdeldycke/click-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
