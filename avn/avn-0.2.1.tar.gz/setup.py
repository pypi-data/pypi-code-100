# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avn']

package_data = \
{'': ['*']}

install_requires = \
['librosa==0.8.0',
 'matplotlib>=3.4.1,<4.0.0',
 'more_itertools>=8.5.0,<9.0.0',
 'numpy>=1.20.2,<1.21.0',
 'pandas>=1.3.3',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.6.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'avn',
    'version': '0.2.1',
    'description': 'Package for zebra finch song analysis.',
    'long_description': "# avn \n\n[![Python](https://img.shields.io/badge/python-3.9-blue)]()\n[![codecov](https://codecov.io/gh/theresekoch/avn/branch/main/graph/badge.svg)](https://codecov.io/gh/theresekoch/avn)\n[![Documentation Status](https://readthedocs.org/projects/avn/badge/?version=latest)](https://avn.readthedocs.io/en/latest/?badge=latest)\n\n`avn` (Avian Vocalization Network, pronounced 'avian') is a python package for zebra finch song analysis. It currently provides functions\nnecessary for threshold-based song segmentation into syllables, with plans for more features in the future. \n\n## Installation\n\n```bash\n$ pip install avn\n```\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://avn.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/theresekoch/avn/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n",
    'author': 'Therese Koch',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theresekoch/avn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
