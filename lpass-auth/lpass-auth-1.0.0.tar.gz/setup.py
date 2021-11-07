# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lpass_auth']

package_data = \
{'': ['*']}

install_requires = \
['SecretStorage>=3.3.1,<4.0.0',
 'keyring>=23.2.1,<24.0.0',
 'pycryptodome>=3.11.0,<4.0.0',
 'pyotp>=2.6.0,<3.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['lpass-auth = lpass_auth.cli:main']}

setup_kwargs = {
    'name': 'lpass-auth',
    'version': '1.0.0',
    'description': 'A command-line client for LastPass Authenticator.',
    'long_description': '# lpass-auth\n\n> A [LastPass Authenticator][authenticator] client written in Python\nheavily inspired by [lastpass-cli][lastpass-cli] and based on \n[code by Donny Maasland][export].\n\n## Installation\n\n### Git\n```bash\ngit clone https://github.com/supersonichub1/lpass-auth\ncd lpass-auth\npoetry install\n```\n\n### pip\n```bash\npip install -U lpass-auth\n```\n\n## Help\nRun `lpass-auth --help` for the most up-to-date information.\n\n### `show --format`\nThe `show` subcommand allows for the customization of the command\'s output\nthrough the `--format` option, a la `lpass show --format`. \nInstead of using `printf`-like formatting, `lpass-auth` instead uses \n[Python\'s format string syntax][format-string], which I believe is much\nmore intuitive and user friendly.\n\nThe format string supplies the following values:\n* accountID\n* digits\n* issuerName\n* lmiUserId\n* originaIssuerName\n* originalUserName\n* pushNotification\n* secret\n* timeStep\n* userName\n\nFor example:\n```bash\n$ lpass-auth show --issuer LastPass \\\n--format "{accountID} ({login}): {password}" \\\nLastPass (example@example.com): 690420\n```\n\n## Caveots\n* only supports no authentication or TOTP authentication; sorry Yubikey users!\n* cannot add or remove passwords due to lack of API knowledge\n\n## TODO\n* error handling\n* dump/export passwords a la [lastpass-authenticator-export][export]\n\n[authenticator]: https://www.lastpass.com/solutions/authentication/two-factor-authentication\n[lastpass-cli]: https://github.com/lastpass/lastpass-cli\n[export]: https://github.com/dmaasland/lastpass-authenticator-export\n[format-string]: https://docs.python.org/3/library/string.html#format-string-syntax\n',
    'author': 'Kyle Anthony Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SuperSonicHub1/lpass-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
