# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketutils',
 'pocketutils.biochem',
 'pocketutils.core',
 'pocketutils.misc',
 'pocketutils.plotting',
 'pocketutils.tools']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7,<1.0',
 'orjson>=3.4,<4.0',
 'regex>=2021',
 'toml>=0.10,<1.0',
 'tomlkit>=0.7,<1.0']

extras_require = \
{'all': ['loguru>=0.5,<1.0',
         'joblib>=1,<2',
         'numpy>=1.19,<2.0',
         'pandas>=1.2,<2.0',
         'pint>=0.17,<1.0',
         'matplotlib>=3.3,<4.0',
         'goatools>=1,<2',
         'requests>=2,<3',
         'uniprot>=1.3,<2.0',
         'psutil>=5,<6',
         'typer>=0.4,<1.0',
         'ipython>=7.0'],
 'biochem': ['numpy>=1.19,<2.0',
             'pandas>=1.2,<2.0',
             'pint>=0.17,<1.0',
             'goatools>=1,<2',
             'requests>=2,<3',
             'uniprot>=1.3,<2.0'],
 'misc': ['psutil>=5,<6', 'typer>=0.4,<1.0'],
 'notebooks': ['pandas>=1.2,<2.0', 'ipython>=7.0'],
 'plotting': ['numpy>=1.19,<2.0', 'pandas>=1.2,<2.0', 'matplotlib>=3.3,<4.0'],
 'tools': ['loguru>=0.5,<1.0',
           'joblib>=1,<2',
           'numpy>=1.19,<2.0',
           'pandas>=1.2,<2.0',
           'pint>=0.17,<1.0']}

setup_kwargs = {
    'name': 'pocketutils',
    'version': '0.8.3',
    'description': 'Adorable little Python code for you to copy or import.',
    'long_description': '# pocketutils\n\n[![Version status](https://img.shields.io/pypi/status/pocketutils?label=status)](https://pypi.org/project/pocketutils)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/pocketutils?label=Python)](https://pypi.org/project/pocketutils)\n[![Version on Docker Hub](https://img.shields.io/docker/v/dmyersturnbull/pocketutils?color=green&label=Docker%20Hub)](https://hub.docker.com/repository/docker/dmyersturnbull/pocketutils)\n[![Version on Github](https://img.shields.io/github/v/release/dmyersturnbull/pocketutils?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/pocketutils/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/pocketutils?label=PyPi)](https://pypi.org/project/pocketutils)  \n[![Build (Actions)](https://img.shields.io/github/workflow/status/dmyersturnbull/pocketutils/Build%20&%20test?label=Tests)](https://github.com/dmyersturnbull/pocketutils/actions)\n[![Documentation status](https://readthedocs.org/projects/pocketutils/badge)](https://pocketutils.readthedocs.io/en/stable/)\n[![Coverage (coveralls)](https://coveralls.io/repos/github/dmyersturnbull/pocketutils/badge.svg?branch=main&service=github)](https://coveralls.io/github/dmyersturnbull/pocketutils?branch=main)\n[![Maintainability (Code Climate)](https://api.codeclimate.com/v1/badges/eea2b741dbbbb74ad18a/maintainability)](https://codeclimate.com/github/dmyersturnbull/pocketutils/maintainability)\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dmyersturnbull/pocketutils/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/dmyersturnbull/pocketutils/?branch=main)\n\nAdorable little Python functions for you to copy or import.\n\n`pip install pocketutils` or\n`pip install pocketutils[all]`\n[Apache](https://spdx.org/licenses/Apache-2.0.html)-licensed.\n\n### Basic usage – `Tools`\n\n```python\nfrom pocketutils.full import Tools\n\nTools.zip_strict([1, 2, 3], [5, 6])  # error <-- lengths must match\nTools.strip_brackets("( (xy)")  # "(xy" <-- strips paired only\nTools.sanitize_path("x\\ty")  # "xy"  <-- very robust cross-platform sanitization\nTools.delete_surefire("my_file")  # <-- Attempts to fix permissions if needed\nTools.git_description("my_repo").tag  # <-- get git repo info\nTools.pretty_function(lambda s: None)  # "<λ(1)> <-- decent name for any object\nTools.roman_to_arabic("XIV")  # 14  <-- inverse function too\nTools.delta_time_to_str(delta_sec=60 * 2 + 5)  # "02:05"  <-- handles days too\nTools.round_to_sigfigs(135.3, 2)  # 140  <-- rounding to sigfigs-proper\nTools.pretty_float(-float("-inf"))  # "−∞"  <-- proper unicode, no trailing 0s\nTools.stream_cmd_call(["cat", "big-file"], callback=fn)  # <-- buffer never fills\nTools.strip_off("hippopotamus", "hippo")  # "potamus"  <-- what .strip() should do\nTools.strip_quotes("\'hello\'")  # "hello"\nTools.truncate10("looong string")  # "looong st…"\nTools.parse_bool("true")  # True\nTools.parse_bool_flex("yes")  # True\nTools.look(item, "purchase.buyer.first_name")  # None if purchase or buyer is None\nTools.friendly_size(n_bytes=2 * 14)  # "16.38 kb"\nTools.is_probable_null("NaN")  # True\nTools.is_true_iterable("kitten")  # False\nTools.or_null(some_function)  # None if it fails\nTools.or_raise(None)  # raises an error (of your choice)\nTools.trash(unwanted_file)  # move to os-specific trash\nTools.pretty_dict({"contents": {"greeting": "hi"}})  # indented\nTools.save_diagnostics(Tools.get_env_info())  # record diagnostic info\nTools.is_lambda(lambda: None)  # True\nTools.longest(["a", "a+b"])  # "a+b"  # anything with len\nTools.only([1, 2])  # error -- multiple items\nTools.first(iter([]))  # None <-- better than try: next(iter(x)) except:...\n# lots of others\n```\n\n### More things\n\n- `FancyLoguru` (really useful)\n- `NestedDotDict` (esp. for toml and json)\n- `QueryUtils` (handles rate-limiting, etc.)\n- `FigTools` (for matplotlib)\n- `J` (tools to interact with Jupyter)\n- `WB1` (microwell plate nomenclature)\n- `Chars` (e.g. `Chars.shelled(s)` or `Chars.snowflake`)\n- `exceptions` (general-purpose exceptions that can store relevant info)\n\n_Even more, albeit more obscure:_\n\n- `TissueExpression`, `UniprotGo`, `AtcTree`, `PlateRois`\n- `WebResource`, `magic_template`\n- `color_schemes`, `FigSaver`, `RefDims`\n- `LoopTools`\n- `MemCache`\n\n[See the docs 📚](https://pocketutils.readthedocs.io/en/stable/), or just\n[browse the code](https://github.com/dmyersturnbull/pocketutils/tree/main/pocketutils).\n[New issues](https://github.com/dmyersturnbull/pocketutils/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/pocketutils/blob/main/CONTRIBUTING.md)\nand [security policy](https://github.com/dmyersturnbull/pocketutils/blob/main/SECURITY.md).  \nGenerated with tyrannosaurus: `tyrannosaurus new tyrannosaurus`\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/pocketutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
