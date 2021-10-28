# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shinyutils']

package_data = \
{'': ['*'], 'shinyutils': ['data/*']}

install_requires = \
['corgy>=1.4,<2.0']

extras_require = \
{'color': ['rich>=10.0,<11.0'],
 'plotting': ['matplotlib>=3.0,<4.0', 'seaborn>=0.10,<0.11'],
 'pytorch': ['torch>=1.5,<2.0',
             'torchvision',
             'tensorboard[python]>=2.0,<3.0',
             'tqdm>=4.4,<5.0']}

setup_kwargs = {
    'name': 'shinyutils',
    'version': '9.1.0',
    'description': 'Personal collection of common utilities',
    'long_description': '# shinyutils\nVarious utilities for common tasks. :sparkles: :sparkles: :sparkles:\n\n## Setup\nInstall with `pip` (Python 3.7 or higher is required). Additional features can be enabled with the `[<feature>]` syntax shown below. Available optional features are:\n\n* `color`: color support for logging\n\n* `plotting`: support for `matplotlib` and `seaborn` (`shinyutils.matwrap` module)\n\n* `pytorch`: support for `pytorch` (`shinyutils.pt` module)\n\n```bash\npip install shinyutils  # basic install\npip install "shinyutils[color]"  # install with color support\npip install "shinyutils[color,plotting,pytorch]"  # install with all optional features\n```\n\n## Usage\nFor documentation on usage, refer to docs/index.md.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jayanthkoushik/shinyutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
