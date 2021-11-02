# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kpsh', 'kpsh.autotype']

package_data = \
{'': ['*']}

install_requires = \
['prompt_toolkit>=3.0.21,<4.0.0', 'pykeepass>=4.0.0,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['kpsh = kpsh.app:main']}

scripts = \
['contrib/kpsh-client', 'contrib/kpsh-detect-backend-sway', 'contrib/kpsh-menu']

setup_kwargs = {
    'name': 'kpsh',
    'version': '1.0.0',
    'description': 'KeePass shell interface and daemon',
    'long_description': '# kpsh\n\nkpsh, or KeePass Shell, is a password manager and an interactive shell for\nworking directly with KeePass password database files.\n\n## Features\n\n- create, open, lock and unlock databases\n- add, edit and delete database entries\n- list contents of database\n- show contents of database entries and filter them by fields\n- autotype usernames and passwords or any sequences of entry fields (by\n  xdotool on X11 and ydotool on Wayland)\n- access all commands non-interactively via `-c` switch or by piping commands\n  directly to kpsh\n- tab-completion in interactive mode\n- daemon mode: open and unlock your database once and then quickly access\n  its contents from kpsh-client.\n- several built-in ways to obtain a password, which can be passed by argument,\n  typed directly to kpsh or through pinentry program program or fetched from a\n  provided command output\n- ships with highly customizable kpsh-menu script which performs any kpsh\n  command on entries selected by dmenu/rofi/fzf (e.g. autotype passwords\n  selected in dmenu/rofi)\n\n# Usage examples\n\nTypical session:\n\n```\n$ kpsh passwords.kdbx\n\npasswords.kdbx> ls\nPassword: ********\npersonal/bank\npersonal/login\npersonal/website\nwork/login\n\npasswords.kdbx> show work/login\npath: work/login\nusername: John Doe\npassword: jsdf7y8h8349yhj3h42\nnotes[1]: this is my work password\nnotes[2]: it\'s the best\n```\n\nGet a password from gpg-encrypted file (trailing newline, which isn\'t a part\nof password is trimmed):\n\n```\n$ gpg --encrypt -o masterpass.gpg -r mymail@example.com\n<type type type>\n^D\n$ kpsh passwords.kdbx --pw-cmd "gpg --decrypt masterpass.gpg | tr -d \'\\n\'"\n```\n\n... or from a keyring:\n\n```\n$ secret-tool store --label=\'keepass\' database passwords.kdbx\n$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"\n```\n\nAutotype a user/password sequence:\n\n```\n$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"\n                      -c autotype entry1\n```\n\n... or just a password, but a little faster:\n\n```\n$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"\n                      -c "autotype -s {PASSWORD} -D 12 entry1"\n```\n\nRun as daemon (`-d`):\n\n```\n$ kpsh passwords.kdbx -d --pw-cmd "secret-tool lookup database passwords.kdbx" &\n$ kpsh-client ls\nentry1\nentry2\n$ kpsh-client autotype entry1\n```\n\nUse pinentry to get a password when database will be unlocked:\n\n```\n$ kpsh passwords.kdbx --pinentry /usr/bin/pinentry\n```\n\n## Installation\n\nUse [pipx][pipx]:\n\n```\n$ pipx install kpsh\n```\n\nOr directly pip:\n\n```\n$ pip install --user kpsh\n```\n\n  [pipx]: https://github.com/pypa/pipx\n',
    'author': 'Michal Goral',
    'author_email': 'dev@goral.net.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.goral.net.pl/mgoral/keepass-shell',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'scripts': scripts,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
