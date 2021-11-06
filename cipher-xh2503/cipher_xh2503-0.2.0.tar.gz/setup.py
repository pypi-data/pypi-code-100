# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cipher_xh2503']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'cipher-xh2503',
    'version': '0.2.0',
    'description': 'A package for doing great things!',
    'long_description': '# cipher_xh2503\n\nA package for doing great things!\n\n## Installation\n\n```bash\n$ pip install cipher_xh2503\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cipher_xh2503` was created by Xaingyu Han. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cipher_xh2503` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Xiangyu Han',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
