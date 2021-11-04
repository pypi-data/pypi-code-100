# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bfg', 'tests']

package_data = \
{'': ['*'], 'tests': ['negative/*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0', 'fire==0.4.0', 'pathvalidate>=2.5.0,<3.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['bfg = bfg.bfg:main']}

setup_kwargs = {
    'name': 'btrfsgit',
    'version': '9000.0.2',
    'description': 'B-tree Filesystem Git attempts to enable git-like workflow for BTRFS subvolumes. Commit, push, checkout, stash, pull...',
    'long_description': '# BFG\nB-tree Filesystem Git attempts to enable git-like workflow for subvolumes. Commit, push, checkout, stash, pull..\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/btrfsgit">\n    <img src="https://img.shields.io/pypi/v/btrfsgit.svg"\n        alt = "Release Status">\n</a>\n\n\n## user install:\n```pip install --user BtrFsGit```\n\n\n## dev install:\n```\npip install --user poetry\n`cd BtrFsGit\npoetry install # only installs the executable into somewhere like `/.cache/pypoetry/virtualenvs/bfg-iXQCHChq-py3.6/bin/`. It just doesn\'t have a "development mode" like setuptools have with `pip install -e .`. So find that directory, and copy the `bfg` into your `~/.local/bin/`. But that\'s about to be [fixed soon](https://github.com/python-poetry/poetry/issues/34).\n```\n\n\n\n## status\nUndertested, but `commit_and_push_and_checkout`, `remote_commit_and_pull` and other commands work. python-fire (the CLI lib) behaves in unexpected ways sometimes. Data loss could occur ;)\n\n## why\nI built this because my scenario is not just simple backup, but also transfering subvolumes back and forth between multiple machines, where no one machine is a single source of truth. In other words, a desktop computer and a notebook, and a subvol with a bunch of VM images. And then maybe a bunch of external backup HDDs.\n\n## cool features\n* It tries to figure out shared parents smartly, by walking the uuids of subvolumes of both filesystems. It doesn\'t just expect the last transferred snapshot to "be there", in a fixed location, like other tools do.\n* No config files, just specify a source subvol and a target subvol (and the ID 5 mount point) on the command line, and in case of a remote machine, a ssh command to use.\n\n## what this doesn\'s do (yet?)\n* snapshot pruning\n* cleanup after failure / .tmp destination\n* finding shared parent by simply listing the snapshots dirs\n* config files\n\n## todo\n* what happens when there is only an incomplete snapshot on target?\n\n## planned features\n* automatically saving and propagating `sub list` dumps - to allow finding shared parents also for offine generating of send streams, even across multiple machine hops\n* Generating a send stream, and applying it later.\n\n## wishlist\n* some kind of integration with https://github.com/csirac2/snazzer/#snazzer for integrity checks\n* maybe some automation for non-BTRFS backups, ie, create a snapshot, rsync it to an ext4, (and apply snazzer..)\n\n## what this will probably never be\n* an attempt to immitate more of git, like merging, exact same command syntax, commit messages (well maybe commit messages would make sense, maybe as a backend to datalad?)..\n\n\n## example workflow\nthis is how i ping-pong my data between my two machines:\n```\nbfg   \\\n  --YES=true  \\  #  no confirmations\n  --LOCAL_FS_TOP_LEVEL_SUBVOL_MOUNT_POINT=/nvme0n1p6_crypt_root  \\  # ugly hack\n  --sshstr=\'/opt/hpnssh/usr/bin/ssh   -p 2222   -o TCPRcvBufPoll=yes -o NoneSwitch=yes  -o NoneEnabled=yes     koom@10.0.0.20\'  \\\n  commit_and_push_and_checkout  \\  # the command\n  --SUBVOLUME=/d \\  # source\n  --REMOTE_SUBVOLUME=/mx500data/lean  # target\n```\n...this:\n* makes a read-only snapshot of /d/ in /.bfg_snapshots.d/<timestamp>_from_<hostname>\n* finds the best shared parent and sends the snapshot to the other machine over ssh\n* receives it on the other machine in /mx500data/.bfg_snapshots.lean\n* makes a read-only snapshot of /mx500data/lean in /mx500data/.bfg_snapshots.lean/<timestamp>_stash\n* deletes /mx500data/lean\n* makes a read-write snapshot of the received snapshot, in /mx500data/lean\n\n\nAnd back:\n```\nbfg   --YES=true    --REMOTE_FS_TOP_LEVEL_SUBVOL_MOUNT_POINT=/mx500data    --sshstr=\'/opt/hpnssh/usr/bin/ssh   -p 2222   -o TCPRcvBufPoll=yes -o NoneSwitch=yes  -o NoneEnabled=yes     koom@10.0.0.20\'   remote_commit_and_pull   --SUBVOLUME=/d  --REMOTE_SUBVOLUME=/mx500data/lean\n```\nfull output:\n[example_session.md](misc/example_session.md)\n\nsee also:\n[test1](tests/test1.sh)\n\n## available commands\n[docs](docs/bfg/bfg.md)\n\n## prerequisites\n\n### install\nThis isnt a proper python package yet. Python3.8 is expected. Checkout the repo, do\n```\n virtualenv -p /usr/bin/python3.8 venv\n pip install -r requirements.txt\n\n```\n### mount the root\n#### problem\nIf you want to work with subvolumes mounted with `subvol=..`: This is how linux distributions set up your system by default. In this case, BFG would not be able to automatically find the filesystem path of a subvolume given its UUID, so, it wouldn\'t be able to call `btrfs send` with correct `-p` parents.\n#### solution\nmake sure that the root subvolume of your BTRFS filesystem is always mounted. For example my fstab entry:\n```\n/dev/mapper/nvme0n1p6_crypt /nvme0n1p6_crypt_root  btrfs   defaults,subvol=   0   2\n```\nFor some operations, you will need to pass this mountpoint like so: `--LOCAL_FS_TOP_LEVEL_SUBVOL_MOUNT_POINT=...` or `--REMOTE_FS_TOP_LEVEL_SUBVOL_MOUNT_POINT=...`.\n### avoid nested subvolumes\n#### problem\nTo be able to make use of stash and checkout, the subvolume that you want to manage with BFG should not contain other subvolumes, so that it can be `btrfs subvolume delete`\'d without affecting your snapshots or other subvolumes. (or possibly we could just `mv`?)\n#### solution\nAs an example, i have a subvolume `/data`, and by default, BFG will store all snapshots in `/.bfg_snapshots.data`, and i don\'t have snapper doing stuff in `/data/.snapshots`.\n\n### prevent writes to incomplete snapshots\n#### problem\nBTRFS doesn\'t make a subvolume read-only when it\'s `btrfs receive`-ing. If another program writes into it at that time, something bad will happen..\n#### solution\ndon\'t do it!\n\n\n',
    'author': 'koo5',
    'author_email': 'kolman.jindrich@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/koo5/bfg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
