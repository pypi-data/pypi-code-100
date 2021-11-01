# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bump_semver_anywhere']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pytomlpp>=1.0.3,<2.0.0', 'semver>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['bump_semver_anywhere = bump_semver_anywhere.cli:main',
                     'bump_semver_anywhere = bump_semver_anywhere.cli:main']}

setup_kwargs = {
    'name': 'bump-semver-anywhere',
    'version': '0.1.2',
    'description': 'Bump your semantic version of any software using regex',
    'long_description': '# bump semver anywhere\n\nThis is a library intented to replace all semversion bumpers and finally be agnostic of the language / use case for your semantic versioning. This is achieved by providing the regex pattern to the place and filename of the string that contains the semantic version.\n\n## usage\n\n- install `pip install bump_semver_anywhere`\n- create a `bump_semver_anywhere.toml` in the root of your project (see _config example_)\n- run `bump_semver_anywhere -p patch`\n\n### cli\n\n```console\n❯ bump_semver_anywhere --help\nUsage: bump_semver_anywhere [OPTIONS]\n\n  Bump your semantic version of any software using regex\n\nOptions:\n  -c, --config FILE               the config file  [default:\n                                  bump_semver_anywhere.toml]\n  -p, --part [major|minor|patch|prerelease]\n                                  the version part to bump  [required]\n  -n, --dry-run                   do not modify files\n  --help                          Show this message and exit.\n```\n\n## config example\n\nThe following example will bump the version for docker and a python or javascript package.\n\n```toml\n# bump_semver_anywhere.toml\n\n[general]\ncurrent_version = "0.1.0"\n\n[vcs]\ncommit = true\ncommit_msg = "release({part}): bump {current_version} -> {new_version}"\n\n[files]\n\n[files.docker]\nfilename = "docker-compose.yaml"\npattern = \'image:.*?:(.*?)"\'\n\n[files.python-module]\nfilename = "__init__.py"\npattern = \'__version__ ?= ?"(.*?)"\'\n\n[files.python-pyproject]\nfilename = "pyproject.toml"\npattern = \'version ?= ?"(.*?)"\'\n\n[files.javascript]\nfilename = "package.json"\npattern = \'"version": ?"(.*?)"\'\n```\n\n## github action\n\nSee `.github/workflows/bump_semver_anywhere.yaml` to integrate the action to your repo and change `uses: ./` to `uses: scratchmex/bump_semver_anywhere@main`\n\nThe current behaviour is to comment `/release <part>` (e.g. `/release patch`) in a pull request. \nPer default it pushes the bump commit to the branch the PR points to. \nTherefore it should be commented after accepting the PR',
    'author': 'Ivan Gonzalez',
    'author_email': 'scratchmex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scratchmex/all-relative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
