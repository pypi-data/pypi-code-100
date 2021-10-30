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
{'console_scripts': ['create-django-react-app = hybrid_django_react.run:main']}

setup_kwargs = {
    'name': 'hybrid-django-react',
    'version': '0.1.2',
    'description': 'Django starter project template. Dockerized Django serving a static React app',
    'long_description': '# Starter project template: Dockerized hybrid Django React app \nStarter project template using docker to build a Django app that serves React apps statically (as JavaScript files)\n\n## Tech stack\n  - Django (with Rest framework, PostgreSQL, SMTP gmail backend, whitenoise, etc.)\n  - React (bundled with webpack and transpiled with babel)\n  - Docker\n  - Deployment to Heroku\n\n## Prerequisites\n  - Docker\n  - pip, poetry, pyenv or a similar tool to access [pypi](https://pypi.org/)\n\n## Installation\n   Install with the following command\n   ```pip install hybrid-django-react```\n\n## Usage\nRun the scripts with the following command:\n   ````create-django-react-app```\n\nYou will be prompted for some information like project name, email, etc. This data is needed to change the configuration files accordingly\n\nAfter the script has run, you don\'t need this tool anymore :)\n\nSimply start the docker container to start working:\n ```docker-compose up -d```\n\n## Debugging with Docker and VSCode\n\nSupport for debugging remotely with VSCode is supported out-of-the-box.\n\nTo debug with Docker:\n\n1. Run your Docker containers as usual: `docker-compose up -d --build`\n\n3. Start the debug session from VS Code for the `[django:docker] runserver` configuration\n\n   1. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.\n\n   2. Hit the Play button or hit `F5` to start debugging\n\n      - Logs will redirect to your integrated terminal as well.\n\n4. Set some breakpoints in functions or methods executed when needed. Usually it\'s Model methods or View functions\n\n## Adding external libraries\n\nIt\'s better to install external libraries from from Docker directly\n\n### Python libraries:\n   #### Production libraries\n   ```docker-compose exec web poetry add [pip_package]```\n   #### Development libraries\n   ```docker-compose exec web poetry add [pip_package] --dev```\n### JavaScript libraries:\n   #### Production libraries\n   ```docker-compose exec web npm install [npm_package]```\n   #### Development libraries\n   ```docker-compose exec web npm install -D [npm_package]```\n\n## Deploy to Heroku\n### First setup\n1. [Create an account](https://www.heroku.com) and [install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)  \n2. Create a new app on Heroku\n   ````heroku create```\n   Your app will get a randomly generated name, like "lazy-beyond-52146". Let\'s call this name [APP_NAME]\n3. Add environment variables that Django needs to read:\n   1. DJANGO_ENVIRONMENT:\n      ```heroku config:set DJANGO_ENVIRONMENT=production```\n   2. DJANGO_SECRET_KEY:\n      You can create a safe secret key [using this site](https://djecrety.ir/)\n      ```heroku config:set DJANGO_SECRET_KEY=[secret_key]}```\n   3. DJANGO_DEBUG:\n      ```heroku config:set DJANGO_DEBUG=False```\n4. Set the stack to Docker containers using the app\'s name\n   ```heroku stack:setcontainer -a [APP_NAME]```\n5. Create a managed postgresql database on Heroku\n   ```heroku addons:create heroku-postgresql:hobby-dev -a [APP_NAME]```\n6. Create a heroku remote repository and push changes to it\n   ```heroku git:remote -a [APP_NAME]```\n   ```git push heroku main```\n7. Migrate Database and create superuser\n   ```heroku run python manage.py migrate```\n   ```heroku run python manage.py createsuperuser```\n8. After deployment, check that the site\'s [security audit shows no warnings](https://djcheckup.com/)\n\n### Consecutive deployments to production\nDeploy by pushing to Heroku git repository:\n```git push heroku main```\n',
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
