# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workplanner']

package_data = \
{'': ['*']}

install_requires = \
['better-exceptions>=0.3.3,<0.4.0',
 'fastapi',
 'loguru',
 'orjson',
 'peewee>=3.14,<4.0',
 'pendulum',
 'typer>=0.4,<0.5',
 'uvicorn[standart]']

entry_points = \
{'console_scripts': ['workplanner = workplanner.__main__:cli']}

setup_kwargs = {
    'name': 'workplanner',
    'version': '0.1.0',
    'description': 'Microservice for scheduling tasks',
    'long_description': '# Microservice for scheduling tasks\n\n\nSet path to SQLite database file via variable `WORKPLANNER_DATABASE_PATH`\n\n\n\n## Install\n    poetry add workplanner\n\nor\n\n    pip install workplanner\n\n\n## Run\n    workplanner run --help\n    workplanner run\n\nDefault port 14444\n\n[Swagger](https://github.com/swagger-api/swagger-ui): \\\nhttp://127.0.0.1:14444/docs\n\n[Redoc](https://github.com/Redocly/redoc): \\\nhttp://127.0.0.1:14444/redoc\n',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavelmaksimov/work-planner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
