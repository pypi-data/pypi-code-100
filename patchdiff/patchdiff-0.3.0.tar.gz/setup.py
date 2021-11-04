# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patchdiff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'patchdiff',
    'version': '0.3.0',
    'description': 'MIT',
    'long_description': '[![PyPI version](https://badge.fury.io/py/patchdiff.svg)](https://badge.fury.io/py/patchdiff)\n[![CI status](https://github.com/Korijn/patchdiff/workflows/CI/badge.svg)](https://github.com/Korijn/patchdiff/actions)\n\n# Patchdiff 🔍\n\n## Install\n\n`pip install patchdiff`\n\n## Quick-start\n\n```python\nfrom patchdiff import apply, diff, iapply, to_json\n\ninput = {"a": [5, 7, 9, {"a", "b", "c"}], "b": 6}\noutput = {"a": [5, 2, 9, {"b", "c"}], "b": 6, "c": 7}\n\nops, reverse_ops = diff(input, output)\n\nassert apply(input, ops) == output\nassert apply(output, reverse_ops) == input\n\niapply(input, ops)  # apply in-place\nassert input == output\n\nprint(to_json(ops, indent=4))\n# [\n#     {\n#         "op": "add",\n#         "path": "/c",\n#         "value": 7\n#     },\n#     {\n#         "op": "replace",\n#         "path": "/a/1",\n#         "value": 2\n#     },\n#     {\n#         "op": "remove",\n#         "path": "/a/3/a"\n#     }\n# ]\n```\n',
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Korijn/patchdiff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
