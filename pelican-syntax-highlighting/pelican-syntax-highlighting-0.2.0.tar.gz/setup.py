# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.syntax_highlighting']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-syntax-highlighting',
    'version': '0.2.0',
    'description': 'Highlight syntax using Prism.js, Highlight.js or Pygments',
    'long_description': '# Syntax Highlighting: A Plugin for Pelican\n\n[![Build Status](https://github.com/f-koehler/pelican-syntax-highlighting/actions/workflows/main.yml/badge.svg)](https://github.com/f-koehler/pelican-syntax-highlighting/actions/workflows/main.yml)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-syntax-highlighting)](https://pypi.org/project/pelican-syntax-highlighting/)\n![License](https://img.shields.io/pypi/l/pelican-syntax-highlighting?color=blue)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/f-koehler/pelican-syntax-highlighting/main.svg)](https://results.pre-commit.ci/latest/github/f-koehler/pelican-syntax-highlighting/main)\n\nHighlight syntax using Prism.js, Highlight.js or Pygments\n\n## Installation\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-syntax-highlighting\n\n## Usage\n\n<<Add plugin details here>>\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/f-koehler/pelican-syntax-highlighting/issues\n[contributing to pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/pelican-syntax-highlighting',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
