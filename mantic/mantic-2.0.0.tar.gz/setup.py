# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mantic',
 'mantic.actions',
 'mantic.domain',
 'mantic.infra',
 'mantic.infra.repo',
 'mantic.utils',
 'mantic_cli',
 'mantic_cli.tasks',
 'mantic_cli.views',
 'mantic_hypothesis']

package_data = \
{'': ['*']}

install_requires = \
['GitPython<4',
 'classes<1',
 'deal<5',
 'invoke<2',
 'nptyping<2',
 'numpy>=1.7,<1.22',
 'returns<1',
 'rich<11',
 'termcolor<2',
 'toml<1',
 'typical<3']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing_extensions<4']}

entry_points = \
{'console_scripts': ['mantic = mantic_cli:main.run']}

setup_kwargs = {
    'name': 'mantic',
    'version': '2.0.0',
    'description': 'Command-line tools to facilitate se-mantic versioning.',
    'long_description': '[![Test](https://github.com/maukoquiroga/mantic/workflows/test/badge.svg)](https://github.com/maukoquiroga/mantic/actions?workflow=test)\n[![Type](https://github.com/maukoquiroga/mantic/workflows/type/badge.svg)](https://github.com/maukoquiroga/mantic/actions?workflow=type)\n[![Lint](https://github.com/maukoquiroga/mantic/workflows/lint/badge.svg)](https://github.com/maukoquiroga/mantic/actions?workflow=lint)\n[![Docs](https://github.com/maukoquiroga/mantic/workflows/docs/badge.svg)](https://github.com/maukoquiroga/mantic/actions?workflow=docs)\n[![Docs](https://readthedocs.org/projects/mantic/badge/)](https://mantic.readthedocs.io/)\n[![PyPI](https://img.shields.io/pypi/v/mantic.svg)](https://pypi.org/project/mantic/)\n[![Coverage](https://codecov.io/gh/maukoquiroga/mantic/branch/main/graph/badge.svg)](https://codecov.io/gh/maukoquiroga/mantic)\n\n# Mantic\n\nCommand-line tools to facilitate se-mantic versioning!\n\n## Demo\n\n![mantic](https://user-images.githubusercontent.com/329236/137640522-1673fc7e-8d88-4418-b10a-29e1e4a1408a.gif)\n\n## Installation\n\n```\npip install mantic\n```\n\n## Usage\n\n```\nmantic --help\nmantic --help check-version\nmantic check-version\n```\n\n## License\n\nCopyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>\n\nLicensed under the EUPL-1.2-or-later\nFor details: [https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)\n',
    'author': 'Mauko Quiroga',
    'author_email': 'mauko@pm.me',
    'maintainer': 'Mauko Quiroga',
    'maintainer_email': 'mauko@pm.me',
    'url': 'https://github.com/maukoquiroga/mantic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
