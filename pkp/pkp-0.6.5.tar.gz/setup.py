# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pkp']
install_requires = \
['colorama>=0.4.4,<0.5.0', 'pykeepass>=3.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['pkp = pkp:cli_main']}

setup_kwargs = {
    'name': 'pkp',
    'version': '0.6.5',
    'description': 'Straightforward CLI for KeePass - powered by pykeepass',
    'long_description': '# 😸 pkp ⚡⚡\n\n[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pschmitt/pkp)](https://github.com/pschmitt/pkp/releases/latest)\n[![CI](https://github.com/pschmitt/pkp/workflows/CI/badge.svg)](https://github.com/pschmitt/pkp/actions?query=workflow%3A%22CI%22)\n\n`pkp` ([pronunciation](https://www.youtube.com/watch?v=9c0rNjyVbT8)) is a \nsimple CLI tool to query KeePass databases from CLI.\n\nIt\'s built on the awesome \n[pykeepass library](https://github.com/libkeepass/pykeepass).\n\n# Installation\n\n## Binary\n\nThe easiest way to start would be to check out the\n[latest release](https://github.com/pschmitt/pkp/releases/latest).\n\n**NOTE**: The `-termux` binaries are manually built on Termux with \n`./build.sh termux` (no CI).\n\n## zinit\n\n```zsh\n# KeePass\n() {\n  local extra_args=()\n\n  if command -v termux-info > /dev/null\n  then\n    extra_args=(bpick"*termux")\n  fi\n\n  zzinit \\\n    $extra_args \\\n    as"command" \\\n    from"gh-r" \\\n    sbin"pkp* -> pkp" \\\n    for pschmitt/pkp\n}\n```\n\n## From pypi\n\n```shell\n# Recommended\npipx install pkp\n\n# Boring alternative\npip3 install --user pkp\n```\n\n# Usage\n\nJust run `pkp --help`. You\'ll get it:\n\n<!-- PKP_HELP -->\n```\nusage: pkp.py [-h] [-V] -f FILE [-p PASSWORD] [-F KEYFILE] [-I] [-r] [-C] [-D]\n              {list,ls,l,get,g,entry,e,show,display,sh,ds,search,find,fd,se,f,s}\n              ...\n\npositional arguments:\n  {list,ls,l,get,g,entry,e,show,display,sh,ds,search,find,fd,se,f,s}\n                        sub-command help\n    list (ls, l)        List entries (by path)\n    get (g, entry, e)   Get entries\n    show (display, sh, ds)\n                        Show entry data\n    search (find, fd, se, f, s)\n                        Find entries\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         show program\'s version number and exit\n  -f FILE, --file FILE  KeePass DB file\n  -p PASSWORD, --password PASSWORD\n                        Password\n  -F KEYFILE, --keyfile KEYFILE\n                        Key file\n  -I, --case-sensitive  Case sensitive matching\n  -r, --raw             Disable REGEX path search\n  -C, --no-color        Disable colored output\n  -D, --debug           Debug mode\n```\n<!-- PKP_HELP_END -->\n',
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pschmitt/pkp',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
