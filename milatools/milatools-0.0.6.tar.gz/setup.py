# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['milatools']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.18.1,<2.0.0',
 'coleo==0.2.5',
 'ptera==0.4.2',
 'sshconf>=0.2.2,<0.3.0']

entry_points = \
{'console_scripts': ['mila = milatools.commands:main']}

setup_kwargs = {
    'name': 'milatools',
    'version': '0.0.6',
    'description': 'Tools to work with the Mila cluster',
    'long_description': "\n# milatools\n\nThe milatools package provides the `mila` command, which is meant to help with connecting to and interacting with the Mila cluster.\n\n\n## Install\n\nRequires Python >= 3.8\n\n```bash\npip install milatools\n```\n\nOr, for bleeding edge version:\n\n```bash\npip install git+git://github.com/mila-iqia/milatools.git\n```\n\nAfter installing `milatools`, start with `mila init`:\n\n```bash\nmila init\n```\n\n\n## Commands\n\n### mila init\n\nSet up your access to the mila cluster interactively. Have your username and password ready!\n\n* Set up your SSH config for easy connection with `ssh mila`\n* Set up your public key if you don't already have them\n* Copy your public key over to the cluster for passwordless auth\n* Set up a public key on the login node to enable ssh into compute nodes\n\n\n### mila code\n\nConnect a VSCode instance to a compute node. `mila code` first allocates a compute node using slurm (you can pass slurm options as well using `--alloc`), and then calls the `code` command with the appropriate options to start a remote coding session on the allocated node.\n\nYou can simply Ctrl+C the process to end the session.\n\n```\nusage: mila code [-h] [--alloc ...] [--job VALUE] [--node VALUE] PATH\n\npositional arguments:\n  PATH          Path to open on the remote machine\n\noptional arguments:\n  -h, --help    show this help message and exit\n  --alloc ...   Extra options to pass to slurm\n  --job VALUE   Job ID to connect to\n  --node VALUE  Node to connect to\n```\n\nFor example:\n\n```bash\nmila code path/to/my/experiment\n```\n\nThe `--alloc` option may be used to pass extra arguments to `salloc` when allocating a node (for example, `--alloc --gres=cpu:8` to allocate 8 CPUs). `--alloc` should be at the end, because it will take all of the arguments that come after it.\n\nIf you already have an allocation on a compute node, you may use the `--node NODENAME` or `--job JOBID` options to connect to that node.\n",
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mila-iqia/milatools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
