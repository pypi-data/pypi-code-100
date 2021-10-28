# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webknossos',
 'webknossos.annotation',
 'webknossos.client',
 'webknossos.client._generated',
 'webknossos.client._generated.api',
 'webknossos.client._generated.api.datastore',
 'webknossos.client._generated.api.default',
 'webknossos.client._generated.models',
 'webknossos.client._resumable',
 'webknossos.dataset',
 'webknossos.dataset._utils',
 'webknossos.geometry',
 'webknossos.skeleton',
 'webknossos.skeleton.nml']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.1.0,<22.0.0',
 'boltons>=21.0.0,<21.1.0',
 'cattrs==1.7.1',
 'cluster_tools>=1.52,<2.0',
 'httpx>=0.15.4,<0.19.0',
 'loxun>=2.0,<3.0',
 'networkx>=2.6.2,<3.0.0',
 'numpy>=1.15.0,<2.0.0',
 'psutil>=5.6.7,<6.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'rich>=10.9.0,<11.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'scipy>=1.4.0,<2.0.0',
 'typing-extensions>=3.7,<4.0',
 'wkw==1.1.11']

setup_kwargs = {
    'name': 'webknossos',
    'version': '0.8.21',
    'description': 'Python package to work with webKnossos datasets and annotations',
    'long_description': '# webKnossos Python Library\n[![PyPI version](https://img.shields.io/pypi/v/webknossos)](https://pypi.python.org/pypi/webknossos)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/webknossos.svg)](https://pypi.python.org/pypi/webknossos)\n[![Build Status](https://img.shields.io/github/workflow/status/scalableminds/webknossos-libs/CI/master)](https://github.com/scalableminds/webknossos-libs/actions?query=workflow%3A%22CI%22)\n[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg)](https://docs.webknossos.org/webknossos-py)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython API for working with [webKnossos](https://webknossos.org) datasets, annotations, and for webKnossos server interaction.\n\nFor the webKnossos server, please refer to https://github.com/scalableminds/webknossos.\n\n## Features\n\n- easy-to-use dataset API for reading/writing/editing raw 2D/3D image data and volume annotations/segmentation in webKnossos wrap (*.wkw) format\n    - add/remove layers\n    - update metadata (`datasource-properties.json`) \n    - up/downsample layers\n    - compress layers \n    - add/remove magnifications\n    - execute any of the `wkCuber` operations from your code\n- manipulation of webKnossos skeleton annotations (*.nml) as Python objects\n    - access to nodes, comments, trees, bounding boxes, metadata, etc.\n    - create new skeleton annotation from Graph structures or Python objects\n- interaction, connection & scripting with your webKnossos instance over the REST API\n    - up- & downloading annotations and datasets\n\nPlease refer to [the documentation for further instructions](https://docs.webknossos.org/webknossos-py).\n\n## Installation\nThe `webknossos` package requires at least Python 3.7+.\n\nYou can install it from [pypi](https://pypi.org/project/webknossos/), e.g. via pip:\n\n```bash\npip install webknossos\n```\n\n## Examples\nSee the [examples folder](examples) or the [the documentation](https://docs.webknossos.org/webknossos-py).\n\n## License\n[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)\nCopyright [scalable minds](https://scalableminds.com)\n',
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
