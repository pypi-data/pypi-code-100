# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['charmonium', 'charmonium.async_subprocess']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'charmonium.async-subprocess',
    'version': '0.1.1',
    'description': 'async clone of subprocess.run',
    'long_description': 'charmonium.async_subprocess\n===========================\n\nSee the documentation of the main function::\n\n   async def run(\n       args: Sequence[StrBytes],\n       cwd: Optional[Path] = None,\n       env: Optional[Union[Mapping[StrBytes, StrBytes]]] = None,\n       env_override: Optional[Mapping[StrBytes, StrBytes]] = None,\n       capture_output: bool = False,\n       check: bool = False,\n       text: Optional[bool] = None,\n   ) -> subprocess.CompletedProcess:\n       """An async clone of `subprocess.run`.\n   \n       Suppose you have Python script that orchestrates shell commands,\n       but it\'s too slow, and you\'ve identified commands which can run in\n       parallel. You could use `threading`, but that has GIL problems, or\n       `multiprocess`, which has a high startup-cost per worker. You are\n       already spinning off subprocesses, which the OS will run\n       concurrently, so why not use async/await programming to express\n       concurrency in a single thread?\n   \n       Note this function does not permit you to communicate\n       asynchronously, just to run commands asynchronously.\n   \n       This function supports a subset of the signature of\n       `subprocess.run`, that I will expand based on need. If you need\n       some functionality, submit an issue or PR.\n   \n       """\n',
    'author': 'Samuel Grayson',
    'author_email': 'sam@samgrayson.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/charmoniumQ/charmonium.async_subprocess.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
