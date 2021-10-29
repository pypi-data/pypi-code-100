# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aflowey']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'aflowey',
    'version': '0.0.15',
    'description': 'Async flow made easy and fun',
    'long_description': 'Aflowey\n========\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/aflowey.svg\n   :target: https://pypi.org/project/aflowey/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/aflowey.svg\n   :target: https://pypi.org/project/aflowey/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/aflowey\n   :target: https://pypi.org/project/aflowey\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/aflowey\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/aflowey/latest.svg?label=Read%20the%20Docs\n   :target: https://aflowey.readthedocs.io/\n   :alt: Read the documentation at https://aflowey.readthedocs.io/\n.. |Tests| image:: https://github.com/jerkos/aflowey/workflows/Tests/badge.svg\n   :target: https://github.com/jerkos/aflow/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/jerkos/aflowey/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/jerkos/aflowey\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Utilities to describe and execute flow with coroutine functions\n* Easily launch several flows simultaneously\n* Strong focus on readability\n\nhttps://aflowey.readthedocs.io\n\nRequirements\n------------\n\n* python 3.9 +\n\nThis library is easier to use with third party libraries for manipulating function\nsuch as fn_ (flip function, function composition...), and tenacity_ (retry library).\n\n\nInstallation\n------------\n\nYou can install *Aflowey* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install aflowey\n\n\nUsage\n-----\n\nChain function to execute an async flow !\n\n\n.. code:: python\n\n    from aflowey import aflow, CANCEL_FLOW, aexec, flog, lift\n\n    db = ... # get client db\n\n    # add some other library\n    from tenacity import retry\n\n    async def fetch_url(url):\n        return await ...\n\n    def process_data(html):\n        processed_data = ...  # process data\n        if processed_data is None:\n            return CANCEL_FLOW\n\n        return processed_data\n\n    async def insert_into_db(content):\n        return await db.insert_one(content)\n\n    def get_url_flow(url):\n        # defining a flow for working with url\n        return (\n            aflow.from_args("http://goole.fr")\n            >> retry(wait=2)(fetch_url)\n            >> flog("url fetched", print_arg=True)\n            >> process_data  # this one is synchronous but may included in the flow\n            >> insert_into_db\n        )\n\nExecute the flow for one url:\n\n.. code:: python\n\n    result = await get_url_flow("http://google.com/...").run()\n\n\nExecute several flows asynchronously:\n\n.. code:: python\n\n        from fn import flip\n\n        name = "Marco"\n\n        user_flow = (\n            aflow.empty()\n            >> lift(db.find_one, search={"username": name})\n            >> User.from_dict\n            # the impure indicate that this step does not return a new result\n            # i.e the result of User.from_dict will be sended\n            >> impure(lift(flip(setattr), datetime.now(), \'created_at\'))\n        )\n\n        organization_id = "Not employed"\n\n        organization_flow = (\n            aflow.empty()\n            >> lift(db_find_one, search={"organization_id": organization_id})\n            >> Organization.from_dict\n        )\n\n        urls = [\n            "http://google.com/...",\n            "http://google.com/...",\n            "http://google.com/...",\n            "http://google.com/...",\n        ]\n\n        url_flows = [get_url_flow(url) for url in urls]\n\n        # execute all flow with asyncio gather method\n        executor = aexec(url_flows) | user_flow | organization_flow\n        (url1, url2, url3, url4), user, organization = await executor.run()\n\nIt can be boring to create function that exactly matches arity of the flow.\nAflowey provide some higher order functions to help, see:\n\n* lift: use partial to create new method\n* F0: from a 0 argument function, create one argument function to fit the arity of the flow\n* F1: create a new function with an extra parameter to process input of the flow step\n* spread: create a new function which spread an iterable of arguments into the given function\n* spread_kw: create a new function which spread kw arguments into the given function\n\nThe fn library provide other interesting functions like:\n\n* flip\n\nIf you have any other ideas...\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Aflowey* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/jerkos/aflow/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://aflowey.readthedocs.io\n.. _fn: https://github.com/kachayev/fn.py\n.. _tenacity: https://github.com/jd/tenacity\n',
    'author': 'Marc Dubois',
    'author_email': 'cram@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jerkos/aflowey',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
