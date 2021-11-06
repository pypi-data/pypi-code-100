# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cipher_ky2458']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'cipher-ky2458',
    'version': '0.1.1',
    'description': 'Each letter is replaced by a letter some fixed number of positions down the alphabet.',
    'long_description': '# cipher_ky2458\n\nEach letter is replaced by a letter some fixed number of positions down the alphabet.\n\n## Installation\n\n```bash\n$ pip install cipher_ky2458\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cipher_ky2458` was created by Kun Yao. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cipher_ky2458` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Kun Yao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QMSS-G5072-2021/cipher_kun_yao',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
