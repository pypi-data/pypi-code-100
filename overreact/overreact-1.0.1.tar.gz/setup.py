# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['overreact', 'overreact.thermo']

package_data = \
{'': ['*']}

install_requires = \
['cclib>=1.6.3,<2.0.0', 'numpy==1.21.2', 'scipy>=1.4.0,<2.0.0']

extras_require = \
{'cli': ['rich>=10.12.0,<11.0.0'],
 'fast': ['jax>=0.2.24,<0.3.0', 'jaxlib>=0.1.73,<0.2.0'],
 'solvents': ['thermo>=0.2.10,<0.3.0']}

entry_points = \
{'console_scripts': ['overreact = overreact.cli:main']}

setup_kwargs = {
    'name': 'overreact',
    'version': '1.0.1',
    'description': 'Create and analyze chemical microkinetic models built from computational chemistry data. 🧪📈🧑\u200d🔬',
    'long_description': '# Welcome to **overreact**!\n\n<div style="text-align:center;">\n\n![overreact](https://raw.githubusercontent.com/geem-lab/overreact-guide/master/logo.png)\n\n</div>\n\n**overreact** is a _library_ and a _command-line tool_ for creating and\nanalyzing\n[microkinetic models](https://geem-lab.github.io/overreact-guide/#microkinetic).\nData is parsed directly from computational chemistry output files thanks to\n[`cclib`](https://cclib.github.io/) (see the\n[list of supported programs](https://cclib.github.io/#summary)).\n\n## Installation\n\n**overreact** is a Python package, so you can easily install it with `pip`. See\nthe\n[installation instructions](https://geem-lab.github.io/overreact-guide/install.html).\n\n## License\n\n**overreact** is open-source, released under the permissive **MIT license**. See\n[our LICENSE file](https://github.com/geem-lab/overreact/blob/main/LICENSE).\n\n## Citing **overreact**\n\nIf you use **overreact** in your research, please cite:\n\n> F. S. S. Schneider and G. F. Caramori. _**overreact**: a tool for creating and\n> analyzing microkinetic models built from computational chemistry data_.\n> **2021**. Available at: <https://github.com/geem-lab/overreact>.\n\nHere\'s the reference in [BibTeX](http://www.bibtex.org/) format:\n\n<!-- @article{overreact,\n  title = \\textbf{overreact}: a tool for creating and analyzing microkinetic models built from computational chemistry data},\n  author = {Schneider, F. S. S. and Caramori, G. F.},\n  journal={J. Chem. Phys.},\n  volume={155},\n  number={1},\n  pages={0},\n  year = {2021},\n  publisher={American Chemical Society (ACS)},\n  doi={10.1063/1.5058983},\n  url={https://doi.org/10.1063/1.5058983}\n} -->\n\n```bibtex\n@misc{overreact2021,\n  title        = {\n    \\textbf{overreact}: a tool for creating and analyzing microkinetic models\n    built from computational chemistry data, ver. 1.0\n  },\n  author       = {Schneider, F. S. S. and Caramori, G. F.},\n  year         = 2021,\n  howpublished = {\\url{https://github.com/geem-lab/overreact}}\n}\n```\n\nA paper describing **overreact** is currently being prepared. When it is\npublished, the above BibTeX entry will be updated.\n\n## Funding\n\nThis project was developed at the [GEEM lab](https://geem-ufsc.org/)\n([Federal University of Santa Catarina](https://en.ufsc.br/), Brazil), and was\npartially funded by the\n[Brazilian National Council for Scientific and Technological Development (CNPq)](https://cnpq.br/),\ngrant number 140485/2017-1.\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/geem-lab/overreact',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
