# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiohttp_middlewares']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.0,<4.0.0', 'async-timeout>=3.0,<5.0', 'yarl>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'aiohttp-middlewares',
    'version': '1.2.0',
    'description': 'Collection of useful middlewares for aiohttp applications.',
    'long_description': '===================\naiohttp-middlewares\n===================\n\n.. image:: https://github.com/playpauseandstop/aiohttp-middlewares/workflows/ci/badge.svg\n    :target: https://github.com/playpauseandstop/aiohttp-middlewares/actions?query=workflow%3A%22ci%22\n    :alt: CI Workflow\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n    :alt: pre-commit\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\n.. image:: https://img.shields.io/pypi/v/aiohttp-middlewares.svg\n    :target: https://pypi.org/project/aiohttp-middlewares/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/aiohttp-middlewares.svg\n    :target: https://pypi.org/project/aiohttp-middlewares/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/l/aiohttp-middlewares.svg\n    :target: https://github.com/playpauseandstop/aiohttp-middlewares/blob/master/LICENSE\n    :alt: BSD License\n\n.. image:: https://coveralls.io/repos/playpauseandstop/aiohttp-middlewares/badge.svg?branch=master&service=github\n    :target: https://coveralls.io/github/playpauseandstop/aiohttp-middlewares\n    :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/aiohttp-middlewares/badge/?version=latest\n    :target: http://aiohttp-middlewares.readthedocs.org/en/latest/\n    :alt: Documentation\n\nCollection of useful middlewares for\n`aiohttp.web <https://docs.aiohttp.org/en/stable/web.html>`_ applications.\n\n- Works on Python 3.6+\n- Works with aiohttp 3.7+\n- BSD licensed\n- Latest documentation `on Read The Docs\n  <https://aiohttp-middlewares.readthedocs.io/>`_\n- Source, issues, and pull requests `on GitHub\n  <https://github.com/playpauseandstop/aiohttp-middlewares>`_\n\nQuickstart\n==========\n\nBy default ``aiohttp.web`` does not provide `many built-in middlewares\n<https://docs.aiohttp.org/en/stable/web_reference.html#middlewares>`_ for\nstandart web-development needs such as: handling errors, shielding view\nhandlers, or providing CORS headers.\n\n``aiohttp-middlewares`` tries to fix this by providing several middlewares that\naims to cover most common web-development needs.\n\nFor example, to enable CORS headers for ``http://localhost:8081`` origin and\nhandle errors for ``aiohttp.web`` application you need to,\n\n.. code-block:: python\n\n    from aiohttp import web\n    from aiohttp_middlewares import (\n        cors_middleware,\n        error_middleware,\n    )\n\n\n    app = web.Application(\n        middlewares=(\n            cors_middleware(origins=("http://localhost:8081",)),\n            error_middleware(),\n        )\n    )\n\nCheck `documentation <https://aiohttp-middlewares.readthedocs.io/>`_ for\nall available middlewares and available initialization options.\n',
    'author': 'Igor Davydenko',
    'author_email': 'iam@igordavydenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://igordavydenko.com/projects.html#aiohttp-middlewares',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
