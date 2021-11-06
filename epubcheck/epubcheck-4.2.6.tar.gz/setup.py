# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epubcheck', 'epubcheck.samples']

package_data = \
{'': ['*'], 'epubcheck': ['lib/*', 'licenses/*']}

install_requires = \
['tablib', 'xlrd', 'xlwt']

entry_points = \
{'console_scripts': ['epubcheck = epubcheck.cli:main']}

setup_kwargs = {
    'name': 'epubcheck',
    'version': '4.2.6',
    'description': 'Python epubcheck wrapper',
    'long_description': "# Python wrappers and CLI for EpubCheck\n\n> A command line tool and lib that wraps EpubCheck for Python.\n\n\n## Introduction\n\nThe original [EpubCheck](https://github.com/w3c/epubcheck) is the standard\nJava based validation tool for EPUB maintained by\n[DAISY Consortium](https://daisy.org/) on behalf of the\n[W3C](https://www.w3.org/publishing/epubcheck_fundraising), originally\ndeveloped by the [IDPF](http://idpf.org/).\n\nThis package provides a Python libary and command line tool for convenient\nvalidation of  EPUB files by wrapping the original\n[EpubCheck 4.2.6](https://github.com/w3c/epubcheck/releases/tag/v4.2.6).\n\n* Free software: BSD license\n\n## Installation\n\nIf you have Python on your system you can do the usual:\n\n    $ pip install epubcheck\n\n\nYou must have Python & Java installed on your system. The original Java\nEpubCheck command line client itself is bundled in the\n[PyPi](https://pypi.org/project/epubcheck/) package.\n\nThis package is tested with Python 3.6 - 3.10 on Linux, Mac and Windows.\nIt should also work with PyPy.\n\n## Quickstart\n\n\n### Command line usage examples\n\nValidata all epub files in the current directory:\n\n    $ epubcheck\n\nValidate a single EPUB file:\n\n    $ epubcheck /path/to/book.epub\n\nValidate all files in /epubfolder and create a detailed Excel report::\n\n    $ epubcheck /path/epubfolder --xls report.xls\n\nShow command line help::\n\n    $ epubcheck -h\n\n\n### Using epubcheck as a python library\n\n\n```python\nfrom epubcheck import EpubCheck\nresult = EpubCheck('src/epubcheck/samples/invalid.epub')\nprint(result.valid)\nprint(result.messages)\n```\n\n## Documentation\nhttps://epubcheck.readthedocs.io/en/latest/\n\n## Development\n\nIntall [poetry](https://pypi.org/project/poetry/) checkout this repository and run:\n\n    poetry install\n\n\n## Changelog\n\n### [4.2.6] - 2021-11-06\n- Bump versioning to match original epubcheck version\n- Modernize packaging and CI\n- Fix xls and csv export\n- Updated dependencies\n\n### [0.4.3] - 2021-09-28\n- Update the epubcheck.jar to v4.2.6\n- Remove support for < Python 3.6\n\n### [0.4.2] - 2019-08-07\n- Update the epubcheck.jar to v4.2.2 (see: https://github.com/w3c/epubcheck/releases/tag/v4.2.2)\n\n### [0.3.1] - 2016-04-20\n- Added custom PY2/PY3 compat module and removed dependancy on six\n\n### [0.3.0] - 2016-04-10\n- Add commandline support with Excel batch reporting\n- Moved development status from Alpha to Beta\n\n### [0.2.0] - 2016-04-03\n- EpubCheck results as native python objects\n- More documentation\n\n### [0.1.0] - 2016-04-01\n-  First release on PyPI.\n\n\n## Authors & Contributors\n- Titusz Pan - https://github.com/titusz\n- Sean Quinn - https://github.com/swquinn\n- Curtis Smith - https://github.com/csmithd\n\n## Credits\n\nEpubCheck is a project coordinated by [IDPF](http://idpf.org/). Most of the\nEpubCheck functionality comes from the schema validation tool\n[Jing](https://relaxng.org/jclark/jing.html) and schemas that\nwere developed by [IDPF](http://idpf.org/) and\n[DAISY](https://daisy.org/). Initial EpubCheck development was largely\ndone at [Adobe Systems](https://www.adobe.com/).\n",
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/titusz/epubcheck/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
