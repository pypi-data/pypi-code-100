# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foundry',
 'foundry.game',
 'foundry.game.gfx',
 'foundry.game.gfx.drawable',
 'foundry.game.gfx.objects',
 'foundry.game.level',
 'foundry.gui',
 'foundry.smb3parse',
 'foundry.smb3parse.levels',
 'foundry.smb3parse.objects',
 'foundry.smb3parse.util']

package_data = \
{'': ['*'], 'foundry': ['data/*', 'data/icons/*', 'doc/*']}

install_requires = \
['PySide6>=6.2.0,<7.0.0', 'pyqtdarktheme>=0.1.6,<0.2.0']

entry_points = \
{'console_scripts': ['foundry = foundry.main:main']}

setup_kwargs = {
    'name': 'foundry-smb3',
    'version': '0.2.4',
    'description': 'The future of SMB3',
    'long_description': "# Foundry\n\n[![Build Status](https://travis-ci.org/mchlnix/SMB3-Foundry.svg?branch=master)](https://travis-ci.org/mchlnix/SMB3-Foundry)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nFoundry is the leading editor for SMB3.\n- Website: WIP\n- Discord: https://discord.gg/pm87gm7\n- Documentation: WIP\n- Manual: https://github.com/TheJoeSmo/Foundry/blob/master/MANUAL.md\n- Source Code: https://github.com/TheJoeSmo/Foundry\n- Bug Reporting: https://github.com/TheJoeSmo/Foundry/issues\n\nIt provides:\n- A powerful level editor\n\nTesting:\nFoundry uses `Poetry` as its package manager.  WIP.\n\nCall for Contributions\n----------------------\nFoundry is a community driven initiative that relies on your help and expertise.\n\nSmall improvements or fixes are critical to this repository's success.  Issues labeled `good first issue` are a great place to start.  For larger contributions WIP.\n\nYou do not need to be literate with programming to aid Foundry on its journey.  We also need help with:\n- Developing tutorials\n- Creating graphics for our brand and promotional material\n- Translation\n- Outreach and onboarding new contributors\n- Reviewing issues and suggestions\n\nIf you are undecided on where to start, we encourage you to reach out.  You can ask on our Discord or privately through email.\n\nIf you are new to open source projects and want to be caught up to speed, we recommend [this guide](https://opensource.guide/how-to-contribute/)",
    'author': 'TheJoeSmo',
    'author_email': 'joesmo.joesmo12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.10',
}


setup(**setup_kwargs)
