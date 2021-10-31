# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mammut',
 'mammut.apps',
 'mammut.assessment',
 'mammut.common',
 'mammut.common.catalog',
 'mammut.common.corpus',
 'mammut.common.lexicon',
 'mammut.common.storage',
 'mammut.common.synthetic',
 'mammut.common.synthetic.synthetic_corpus_generator',
 'mammut.curriculum',
 'mammut.curriculum.classroom',
 'mammut.curriculum.core',
 'mammut.curriculum.course',
 'mammut.curriculum.lesson',
 'mammut.curriculum.models',
 'mammut.curriculum.models.hugging_face',
 'mammut.curriculum.models.online_models',
 'mammut.curriculum.report',
 'mammut.curriculum.report.errors',
 'mammut.curriculum.report.messages',
 'mammut.curriculum.report.reporters',
 'mammut.data',
 'mammut.linguistics',
 'mammut.mammutctl',
 'mammut.models',
 'mammut.models.imaging',
 'mammut.models.reparameterization',
 'mammut.resources',
 'mammut.resources.ngram',
 'mammut.visualization',
 'mammut.visualization.templates']

package_data = \
{'': ['*']}

install_requires = \
['Augmentor>=0.2.8,<0.3.0',
 'brat-widget>=0.2.5,<0.3.0',
 'chart-studio>=1.1.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'datasets>=1.2.1,<2.0.0',
 'django>=3.0.7,<4.0.0',
 'dynaconf>=3.1.4,<4.0.0',
 'elasticsearch>=7.7.1,<8.0.0',
 'google-api-python-client>=1.9.3,<2.0.0',
 'graphviz>=0.14,<0.15',
 'jupyter>=1.0.0,<2.0.0',
 'kafka-python>=2.0.1,<3.0.0',
 'networkx>=2.5,<3.0',
 'nltk>=3.5,<4.0',
 'oauth2client>=4.1.3,<5.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'packaging>=20.4,<21.0',
 'pandas>=1.0.4,<2.0.0',
 'parsec>=3.5,<4.0',
 'pip>=20.0.0,<21.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pytest-order>=0.10.0,<0.11.0',
 'python-pptx>=0.6.18,<0.7.0',
 'ray>=1.2.0,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'sentencepiece>=0.1.92,<0.2.0',
 'simpleneighbors>=0.1.0,<0.2.0',
 'tensorflow-probability==0.10.0',
 'tensorflow==2.2.0',
 'tensorflow_hub[make_image_classifier]==0.8.0',
 'tf-sentencepiece>=0.1.90,<0.2.0',
 'torch>=1.8.1,<2.0.0',
 'transformers>=4.5.1,<5.0.0',
 'transitions>=0.8.5,<0.9.0',
 'xlrd>=1.2.0,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses==0.6']}

entry_points = \
{'console_scripts': ['mammutctl = src.mammut.mammutctl.mammutctl:main']}

setup_kwargs = {
    'name': 'mammut-py',
    'version': '0.1.0.dev202110311538',
    'description': 'Mammut framework is an open library for computational linguistics.',
    'long_description': '# Mammut-Py\n\n## Installation\n\nUse pip to install the package:\n```\npip install mammut-py\n```\n\n## Development\n\nThe following tools are used in this project:\n- [Poetry](https://python-poetry.org/) is used as package manager.\n- [Nox](https://nox.thea.codes/) is used as automation tool, mainly for testing.\n- [Black](https://black.readthedocs.io/) is the mandatory formatter tool.\n- [PyEnv](https://github.com/pyenv/pyenv/wiki) is recommended as a tool to handle multiple python versions in your machine.\n\nThe library is intended to be compatible with python ~3.6.9, ~3.7.4 and ~3.8.2. But the primary version to support is ~3.8.2.\n\nThe general structure of the project is trying to follow the recommendations\nin [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).\nThe main difference lies in the source code itself which is not constraint to data science code.\n',
    'author': 'Mammut.io',
    'author_email': 'support@mammut.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://doc.mammut.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
