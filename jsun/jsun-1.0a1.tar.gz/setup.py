# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jsun']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['jsun = jsun.__main__:main']}

setup_kwargs = {
    'name': 'jsun',
    'version': '1.0a1',
    'description': 'JSON encoding & decoding with extra features',
    'long_description': '# jsun\n\nThis is an alternative JSON decoder/encoder that supports some extra\nfeatures. It takes a *lot* of inspiration from the `json` module in the\nstandard library and exposes the same high level API: `load`, `loads`,\n`dump`, `dumps`, `JSONDecoder`, and `JSONEncoder`.\n\nIn many cases, `jsun` can be swapped in by installing the package then\nsimply updating imports to use `jsun` instead of `json`.\n\n## Extra decoding features\n\n- Trailing commas\n \n- Line comments starting with //\n \n- All valid Python ints and floats:\n  - Binary, octal, hex\n  - Underscore separators\n  - Unary plus operator\n\n- Math constants:\n  - inf, nan, E, π, PI, τ, TAU\n  - Infinity, NaN\n\n- Literal (unquoted) dates and times:\n  - 2021-06\n  - 2021-06-23\n  - 2021-06-23T12:00\n  - 2021-06-23T12:00Z\n  - 2021-06-23T12:00-07:00\n  - 12:00 (today\'s date at noon)\n\n- Decoding an empty string will produce `None` rather than an exception\n  (an exception will be raised if extras are disabled)\n\n- *All* parsing methods can be overridden if some additional\n  customization is required. In particular, the object and array\n  parsers can be overridden\n\n- A pre-parse method can be provided to handle values before the regular\n  JSON parsers are applied\n\n- A fallback parsing method can be provided to handle additional types\n  of values if none of the default parsers are suitable\n\n- When errors are encountered, specific exceptions are raised (all\n  derived from the built-in `ValueError`)\n\n## Extra encoding features\n\nThe `jsun` encoder is very similar to the standard library encoder (and\nis in fact a subclass of `json.JSONEncoder`). Currently, it supports\nonly a couple of extra features:\n\n- Date objects are converted to ISO format by default\n- Datetime objects are converted to ISO format by default\n\nNOTE: There is some asymmetry here. E.g., date and datetime objects\nshould be converted to literals instead of quoted strings.\n\n## Disabling the extra features\n\n*All* the extra features can be turned off with a flag:\n\n    >>> from jsun import decode\n    >>> decode("[1, 2, 3,]")\n    [1, 2, 3]\n    >>> decode("[1, 2, 3,]", enable_extras=False)\n    <exception traceback>\n\n## Differences between jsun and standard library json\n\n- An empty string input is converted to `None` rather than raising an\n  exception (only if extras are enabled).\n\n- When decoding, instead of `object_hook` and `object_hook_pairs`,\n  there\'s just a single `object_converter` argument. It\'s essentially\n  the same as `object_hook`. `object_hook_pairs` seems unnecessary\n  nowadays since `dict`s are ordered.\n\n- The default object type is `jsun.obj.JSONObject` instead of `dict`. A\n  `JSONObject` is a bucket of properties that can be accessed via dotted\n  or bracket notation. Pass `object_converter=None` to get back\n  `dict`s instead.\n\n## Config files\n\nA bonus feature is that configuration can be loaded from INI files\nwhere the keys are split on dots to create sub-objects and the values\nare encoded as JSON.\n\nThis is quite similar to TOML and some of the features of `jsun`, like\nliteral dates, are inspired by TOML.\n\nThis feature was originally developed in 2014 as part of the\n`django-local-settings` project, about a year and half after TOML was\nfirst released but before I\'d heard of it.\n\n### Differences with TOML\n\n- Parentheses are used instead of quotes to avoid splitting on dots\n- Objects created using `{}` syntax (AKA "inline tables" in TOML) can\n  span multiple lines\n- There are no arrays of tables\n- Others I\'m not thinking of at the moment...\n\n## About the name\n\nMy first choice was `jsonish` but that\'s already taken. My second choice\nwas `jsonesque` but it\'s also taken, and it\'s hard to type. `jsun` is\nnice because it\'s easy to type and easy to swap in for `json` by just\nchanging a single letter.\n\n## Testing\n\nThere\'s a suite of unit tests, which also tests against the JSON checker\nfiles at https://json.org/JSON_checker/. Coverage is currently at 82%.\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/jsun',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
