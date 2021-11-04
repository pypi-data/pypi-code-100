# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gherlint', 'gherlint.checkers', 'gherlint.objectmodel']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'gherkin-official>=22.0.0,<23.0.0',
 'parse>=1.19.0,<2.0.0']

entry_points = \
{'console_scripts': ['gherlint = gherlint.__main__:cli']}

setup_kwargs = {
    'name': 'gherlint',
    'version': '0.4.0',
    'description': 'Linter for Gherkin feature files',
    'long_description': '# gherlint\nLinter for Gherkin feature files, written in Python\n\n## Install\nSimply run ``pip install gherlint``.\n\n## Linting Feature Files\n``gherlint`` comes with a command line interface.\nTo recursively lint all feature files in a directory, run ``gherlint lint``.\n\n## Computing Metrics\n``gherlint`` can also create some metrics for you if you want to know how many features, scenarios and steps you have\nin your test suite. To do so, run ``gherlint stats``.\n\n## Disclaimer\n``gherlint`` is still in an early development phase. New checks will be added over time.\nIf you want to contribute, feel free to open issues suggesting useful checkers, or open a pull request if you want\nto!\n\n## Roadmap\n\nThe following work items are planned for the upcoming releases:\n\n* V0.0.x - V0.1.0:\n    * Parser and object model for feature files\n    * Basic checkers to demonstrate workflow\n    * Basic text based reporter\n* V0.1.x - V1.0: **<-- we are here**\n    * Add more checkers\n    * Add more output formats\n    * Extend object model as necessary for checkers\n    * Reach a stable interface for object model, checkers and reporters\n* V1.x - V2.0:\n    * Support configuration to enable/disable individual messages\n    * Implement plugin architecture to allow users to add custom checkers\n# CHANGELOG\n\n## V0.4.0\nNew checks:\n* ``unused-parameter``\n* ``empty-background``\n* ``outline-could-be-a-scenario``\n* ``consider-using-background``\n* ``examples-outside-scenario-outline``\n* ``duplicated-tag``\n\nOther changes:\n* ``unparseable-file`` is now issued for all nodes that offend the ``gherkin`` parser together with more error information provided by it\n* ``missing-parameter`` now clearly states what parameter is not defined in the examples\n* If ``gherlint`` patches the file contents with a forgotten ``# language`` tag the line numbers for messages\nare no longer shifted\n* Types of ``And`` and ``But`` steps are now inferred correctly\n* New command ``fix-language-tags`` to automatically add or fix missing or incorrect language tags\n* Rename some message codes to have a defined structure: each checker has its own hundreds digit.\n\n## V0.3.0\nNew checks:\n* ``missing-language-tag``\n* ``wrong-language-tag``\n* ``unparseable-file``\n\nOther changes:\n* ``gherlint`` can now automatically detect the language used and make sure that it can parse the files\neven without a ``# language`` token present.\n\n## V0.2.0\nNew checks:\n* ``missing-given-step``\n* ``missing-when-step``\n* ``missing-then-step``\n* ``empty-scenario``\n* ``empty-feature``\n* ``file-has-no-feature``\n* ``missing-parameter``\n\nOther changes:\n* Support for ``Background``\n* Determination of step type independent of language\n* Distinction between ``Scenario`` and ``Scenario Outline`` independent of language\n\n## V0.1.0\nFirst package in alpha status:\n* Parser and object model for feature files\n* Basic checkers to demonstrate workflow\n* Basic text based reporter\n',
    'author': 'Andreas Finkler',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DudeNr33/gherlint',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
