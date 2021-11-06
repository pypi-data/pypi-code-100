# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['project_checks',
 'project_checks.management',
 'project_checks.management.commands']

package_data = \
{'': ['*'], 'project_checks': ['templates/project_checks/*']}

install_requires = \
['django>=2.2,<5.0']

setup_kwargs = {
    'name': 'django-project-checks',
    'version': '0.1.0a1',
    'description': 'Django management commands used to output useful project information.',
    'long_description': "#\xa0Django Project Check\n\nThis is a Django app that provides a mechanism for\n\n## Background\n\nWith a large codebase, and a high velocity team making edits, it can be\ndifficult to keep track of how the codebase is changing over time. A\nclassic issue is people creating new modules / classes in unexpected\nplaces, or ending up with a set of functions that should be in the same\nplace but are spread across multiple locations (often resulting in\n`import` issues). In order to address this we build a small script to\nparse the codebase and dump out a complete listing of all modules,\nclasses and functions. We commit this to the repo, and then run a CI\ncheck to ensure that it's up to date. The net result is that each PR has\nat least one file update which lists which functions have been edited,\nand where. It's like a live update to the index.\n\nThis pattern - dump a text output and add a CI check to enforce its correctness - turns out to be a really useful pattern for keeping control of the codebase, and so we started adding new checks:\n\n- Python functions\n- Django URLs\n- GraphQL schema\n- FSM interactions\n\nThe original function check is a python script (using `ast`) and has no requirement for the Django scaffolding, but the others do, and so they run as management commands, which are then wrapped with a `git diff` script:\n\n```yaml\n- name: Run freeze_django_urls and check for any uncommitted diff\n  run: |\n    python manage.py freeze_django_urls\n    git diff --exit-code 'django_urls.txt'\n```\n\nThis project wraps this pattern into a base management command that can be subclassed for any such requirement. All you need to do is provide a function that returns the contents to be written to the file.\n",
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/poetry-template',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
