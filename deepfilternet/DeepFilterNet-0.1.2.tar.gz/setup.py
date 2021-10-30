# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['df']

package_data = \
{'': ['*'], 'df': ['scripts/*']}

install_requires = \
['DeepFilterLib>=0.1,<0.2', 'loguru>=0.5,<0.6', 'numpy>=1.20,<2.0']

extras_require = \
{'train': ['DeepFilterDataLoader>=0.1,<0.2']}

entry_points = \
{'console_scripts': ['deepFilter = df.enhance:main']}

setup_kwargs = {
    'name': 'deepfilternet',
    'version': '0.1.2',
    'description': 'Noise supression using deep filtering',
    'long_description': None,
    'author': 'Hendrik Schröter',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rikorose/DeepFilterNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
