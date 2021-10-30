# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piso', 'piso.docstrings']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1,<2', 'staircase>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'piso',
    'version': '0.4.0',
    'description': "Pandas Interval Set Operations: methods for set operations for pandas' Interval, IntervalArray and IntervalIndex",
    'long_description': '<p align="center"><a href="https://github.com/staircase-dev/piso"><img src="https://github.com/staircase-dev/piso/blob/master/docs/img/piso_social_transparent.svg" title="piso logo" alt="piso logo"></a></p>\n\n<p align="center">\n    <a href="https://www.python.org/" alt="Python version">\n        <img src="https://img.shields.io/pypi/pyversions/piso" /></a>\n    <a href="https://pypi.org/project/piso/" alt="PyPI version">\n        <img src="https://img.shields.io/pypi/v/piso" /></a>\n    <a href="https://anaconda.org/conda-forge/piso" alt="Conda Forge version">\n        <img src="https://anaconda.org/conda-forge/piso/badges/version.svg?branch=master&kill_cache=1" /></a>\n\t<a href="https://github.com/staircase-dev/piso/actions/workflows/ci.yml" alt="Github CI">\n\t\t<img src="https://github.com/staircase-dev/piso/actions/workflows/ci.yml/badge.svg"/></a>\n    <a href="https://piso.readthedocs.io" alt="Documentation">\n        <img src="https://readthedocs.org/projects/piso/badge/?version=latest" /></a>\n</p>\n\n# piso - pandas interval set operations\n\n**piso** exists to bring set operations (union, intersection, difference + more) to [pandas\'](https://pandas.pydata.org/) interval classes, specifically\n\n    - pandas.Interval\n    - pandas.arrays.IntervalArray\n    - pandas.IntervalIndex\n\nCurrently, there is a lack of such functionality in pandas, although it has been earmarked for development.  Until this eventuates, piso aims to fill the void.  Many of the methods can be used via accessors, which can be registered to `pandas.arrays.IntervalArray` and `pandas.IntervalIndex` classes, for example:\n\n```python\n>>> import pandas as pd\n>>> import piso\n>>> piso.register_accessors()\n\n>>> arr = pd.arrays.IntervalArray.from_tuples(\n...        [(1,5), (3,6), (2,4)]\n...    )\n\n>>> arr.piso.intersection()\n<IntervalArray>\n[(3, 4]]\nLength: 1, closed: right, dtype: interval[int64]\n```\n\nThe domain of the intervals can be either numerical, `pandas.Timestamp` or `pandas.Timedelta`.\n\nA small [case study](https://piso.readthedocs.io/en/latest/user_guide/calendar.html) using piso can be found in the [user guide](https://piso.readthedocs.io/en/latest/user_guide/index.html).  Further examples, and a detailed explanation of functionality, are provided in the [API reference](https://piso.readthedocs.io/en/latest/reference/index.html).\n\nVisit [https://piso.readthedocs.io](https://piso.readthedocs.io/) for the documentation.\n\n## Installation\n\n`piso` can be installed from PyPI or Anaconda.\n\nTo install the latest version from PyPI::\n\n```sh\npython -m pip install piso\n```\n\nTo install the latest version through conda-forge::\n\n```sh\nconda install -c conda-forge piso\n```\n\n## Versioning\n\n[SemVer](http://semver.org/) is used by piso for versioning releases.  For versions available, see the [tags on this repository](https://github.com/staircase-dev/piso/tags).\n\n## License\n\nThis project is licensed under the [MIT License](https://github.com/staircase-dev/piso/blob/master/LICENSE)\n\n## Acknowledgments\n\nCurrently, piso is a pure-python implentation which relies heavily on [staircase](https://www.staircase.dev) and [pandas](https://pandas.pydata.org/).  It is clearly designed to operate as part of the *pandas ecosystem*.  The colours for the piso logo have been assimilated from pandas as a homage, and is not to intended to imply and affiliation with, or endorsement by, pandas.\n\nAdditionally, two classes have been borrowed, almost verbatim, from the pandas source code:\n\n    - `pandas.util._decorators.Appender`\n    - `pandas.core.accessor.CachedAccessor`',
    'author': 'Riley Clement',
    'author_email': 'venaturum@gmail.com',
    'maintainer': 'Riley Clement',
    'maintainer_email': 'venaturum@gmail.com',
    'url': 'https://github.com/staircase-dev/piso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
