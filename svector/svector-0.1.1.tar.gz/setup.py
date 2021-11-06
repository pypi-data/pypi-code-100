# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['svector', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['pyrsistent>=0.17.0']

setup_kwargs = {
    'name': 'svector',
    'version': '0.1.1',
    'description': 'Typesafe immutable datastructure for python. With plenty of methods for fluent functional programming.',
    'long_description': '# Svector\n\nSvector (pronounced Swag-tor) provides extension methods to [pyrsistent](https://github.com/tobgu/pyrsistent) data structures. \nEasily chain your methods confidently with tons of additional methods. Leverage \nthe latest mypy features to spot errors during coding.\n\n\n[![pypi](https://img.shields.io/pypi/v/svector.svg)](https://pypi.org/project/svector)\n[![python](https://img.shields.io/pypi/pyversions/svector.svg)](https://pypi.org/project/svector)\n[![Build Status](https://github.com/thejaminator/svector/actions/workflows/dev.yml/badge.svg)](https://github.com/thejaminator/svector/actions/workflows/dev.yml)\n\n```\npip install svector\n```\n\nImmutable list replacement for python. With postfix methods for easy functional programming.\n\n\n* GitHub: <https://github.com/thejaminator/svector>\n\n\n## Quick Start\nWith mypy installed, easily spot errors when you call the wrong methods on your sequence.\n\n```python\nfrom svector import Svector\n\nmany_strings = Svector.of(["Lucy, Damion, Jon"])  # Svector[str]\nmany_strings.sum()  # Mypy errors with \'Invalid self argument\'. You can\'t sum a sequence of strings!\n\nmany_nums = Svector.of([1, 1.2])\nassert many_nums.sum() == 2.2  # ok!\n\nclass CannotSortMe:\n    def __init__(self, value: int):\n        self.value: int = value\n\nstuff = Svector.of([CannotSortMe(value=1), CannotSortMe(value=1)])\nstuff.sort_by(lambda x: x)  # Mypy errors with \'Cannot be "CannotSortMe"\'. You can\'t sort by the class itself\nstuff.sort_by(lambda x: x.value)  # ok! You can sort by the value\n\nSvector.of([{"i am a dict": "value"}]).distinct_by(\n    lambda x: x\n)  # Mypy errors with \'Cannot be Dict[str, str]. You can\'t hash a dict itself\n```\n\nSvector provides methods that you can chain easily for easier data processing.\n```python\nfrom svector import Svector\n\nSvector.of([-1, 0, 1]).map(\n    lambda x: x if x >= 0 else None).flatten_option()  # Mypy infers Svector[int] correctly\n\nresult = (\n    Svector.of(i for i in range(5000))\n    .map(lambda x: (x % 3, x))\n    .filter(lambda x: x[0] == 0)\n    .for_each_enumerate(lambda idx, element: print(f"{idx}: {element}"))\n    .take(5)\n)\n```\n',
    'author': 'James Chua',
    'author_email': 'chuajamessh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thejaminator/svector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
