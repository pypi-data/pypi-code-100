# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytsviz']

package_data = \
{'': ['*']}

install_requires = \
['colour>=0.1.5,<0.2.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'scipy>=1.4.1,<2.0.0',
 'statsmodels>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'pytsviz',
    'version': '0.1.0',
    'description': 'A suite of tools to quickly analyze and visualize time series data.',
    'long_description': '# pytsviz\n\n![GitHub](https://img.shields.io/github/license/xtreamsrl/pytsviz)\n![GitHub issues](https://img.shields.io/github/issues/xtreamsrl/pytsviz)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xtreamsrl/pytsviz/blob/master/docs/source/notebooks/data_visualization_examples.ipynb)\n[![Downloads](https://pepy.tech/badge/pytsviz)](https://pepy.tech/project/pytsviz)\n[![Documentation Status](https://readthedocs.org/projects/pytsviz/badge/?version=latest)](https://pytsviz.readthedocs.io/en/latest/?badge=latest)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/xtreamsrl/pytsviz/CI?label=tests)\n\n*pytsviz* is a suite of tools to quickly analyze and visualize time series data. It is partially based on the [*tsviz*](https://github.com/xtreamsrl/tsviz) R package.\n\nThe *utils* module contains a set of useful utilities, not strictly related to visualization, we often use (e.g. harmonics computation).\n\nThe *viz* module contains functions for plotting univariate time series, as well as performing quick qualitative analyses such as decompositions, correlations and so on.\n\nSome visualizations mimic the R packages *ggplot2* and *forecast*, as presented in the textbook *Forecasting: principles and practice* by Rob J. Hyndman and George Athanasopoulos.\nThe online version of the text can be found [here](https://otexts.com/fpp3/).\n\n## Install\n\nThe preferred way to install the package is using pip, but you can also download the code and install from source\n\nTo install the package using pip:\n\n```shell\npip install pytsviz\n```\n\n## Develop\n\nAfter cloning, you need to install and setup Poetry. See [instructions](https://github.com/python-poetry/poetry#installation).\n\nThen, inside the project directory, run:\n\n```shell\npoetry install\npre-commit install\n```\n\nThen, you\'re good to go.\n\nYou\'re free to submit your pull requests. Just make sure they follow [conventional commit rules](https://www.conventionalcommits.org/en/v1.0.0/#specification). This can be enforced by the [*commitizen*](https://commitizen-tools.github.io/commitizen/) tool, which is also included among the package dependencies.\n\nPlease also make sure that function documentation is consistent. We are currently using [Sphinx docstrings](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).\n\n\n## Who we are\n<img align="left" width="80" height="80" src="https://avatars2.githubusercontent.com/u/38501645?s=450&u=1eb7348ca81f5cd27ce9c02e689f518d903852b1&v=4">\nA proudly 🇮🇹 software development and data science startup.<br>We consider ourselves a family of talented and passionate people building their own products and powerful solutions for our clients. Get to know us more on <a target="_blank" href="https://xtreamers.io">xtreamers.io</a> or follow us on <a target="_blank" href="https://it.linkedin.com/company/xtream-srl">LinkedIn</a>.',
    'author': 'xtream',
    'author_email': 'oss@xtreamers.io',
    'maintainer': 'xtream',
    'maintainer_email': 'oss@xtreamers.io',
    'url': 'https://github.com/xtreamsrl/pytsviz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
