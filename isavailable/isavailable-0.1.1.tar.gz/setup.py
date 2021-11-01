# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isavailable']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['isavailable = isavailable:main']}

setup_kwargs = {
    'name': 'isavailable',
    'version': '0.1.1',
    'description': 'Check Python package distribution name availability on PyPI',
    'long_description': '# 😻 isavailable\n\n> Can I haz this Python package on [PyPI][pypi]?\n\n![Can I haz this Python package on PyPI?](i-can-haz-please.jpg)\n\nCheck if Python package names are available on [PyPI][pypi].\n\n[pypi]: https://pypi.org/\n\n## Usage\n\n```bash\n$ isavailable checks whether your desired package name is available on pypi\nis        is… not available 😭 on PyPI.\non        is… not available 😭 on PyPI.\nyour      is… not available 😭 on PyPI.\nname      is…     available 🎉 on PyPI.\npypi      is… not available 😭 on PyPI.\nchecks    is… not available 😭 on PyPI.\nwhether   is…     available 🎉 on PyPI.\ndesired   is…     available 🎉 on PyPI.\npackage   is… not available 😭 on PyPI.\navailable is…     available 🎉 on PyPI.\n```\n\n## Installation\n\n```bash\n$ pip install isavailable\n```\n\n## Help\n\n```bash\n$ isavailable --help\nUsage: isavailable [OPTIONS] NAMES...\n\n  Check if a list of package names are available on PyPI.\n\nArguments:\n  NAMES...  [required]\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schneiderfelipe/isavailable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
