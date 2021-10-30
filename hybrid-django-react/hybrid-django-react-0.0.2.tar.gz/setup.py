# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hybrid_django_react']

package_data = \
{'': ['*'],
 'hybrid_django_react': ['assets/*',
                         'assets/.vscode/*',
                         'assets/frontend/*',
                         'assets/locale/*',
                         'assets/static/*',
                         'assets/templates/*']}

entry_points = \
{'console_scripts': ['run = hybrid_django_react:run.py:main']}

setup_kwargs = {
    'name': 'hybrid-django-react',
    'version': '0.0.2',
    'description': 'Django starter project template. Dockerized Django serving a static React app',
    'long_description': '# Starter project template: Dockerized hybrid Django React app \nStarter project template using docker to build a Django app that serves React apps statically (as JavaScript files)\n\nStack:\n  - Django (with Rest framework, PostgreSQL, SMTP gmail backend, whitenoise, etc.)\n  - React (bundled with webpack and transpiled with babel)\n  - Docker\n  - Deployment to Heroku\n\n## First Setup\n\n1. Make sure poetry is installed `pip install poetry`\n2. Execute `python setup/run.py` or `py setup\\run.py`\n3. After the project is setup, start the docker container to start working `docker-compose up -d`. The "setup" folder will delete itself after setting up the project, as to leave a cleaner project.\n\n## Debugging with Docker and VSCode\n\nSupport for debugging remotely if you\'re running with Docker is supported out-of-the-box.\n\nTo debug with Docker:\n\n1. Rebuild and run your Docker containers as usual: `docker-compose up --build`\n\n3. Start the debug session from VS Code for the `[django:docker] runserver` configuration\n\n   1. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.\n\n   3. Hit the Play button or hit `F5` to start debugging\n\n      - Logs will redirect to your integrated terminal as well.\n\n4. Set some breakpoints in functions or methods executed when needed. Usually it\'s Model methods or View functions\n\n## Adding external libraries\n\nIt\'s better to install external libraries from from Docker directly\n\n1. Python libraries:\n   1. `docker-compose exec web poetry add [pip_package]` for production libraries\n      - Example: `docker-compose exec web poetry add django-extensions`\n   2. `docker-compose exec web poetry add [pip_package] --dev` for development libraries\n      - Example: `docker-compose exec web poetry add --dev selenium`\n2. JavaScript libraries:\n   1. `docker-compose exec web npm install [npm_package]` for production libraries\n      - Example: `docker-compose exec web npm install lodash`\n   2. `docker-compose exec web npm install -D [npm_package]` for development libraries\n      - Example: `docker-compose exec web npm install -D jest`\n\n## Deploy to Heroku\n### First setup\nFollowed guide of "Django for professionals" book\n\n### Consecutive deployments to production\nDeploy by pushing to Heroku git repository:\n```git push heroku main```\n',
    'author': 'gmso',
    'author_email': 'german.mene@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gmso/hybrid-django-react',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
