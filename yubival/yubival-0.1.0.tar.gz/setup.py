# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yubival', 'yubival.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.0,<4.0.0', 'YubiOTP>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'yubival',
    'version': '0.1.0',
    'description': 'Django app that runs a standalone Yubikey validation server',
    'long_description': '![Default branch test status](https://github.com/bruot/yubival/actions/workflows/test.yml/badge.svg)\n![main branch coverage](https://codecov.io/gh/bruot/yubival/branch/main/graph/badge.svg?token=PNVDEEOHTU)\n\n\n# Yubival\n\nThis Django app runs a standalone Yubikey OTP validation server. It implements [version 2.0 of the validation protocol](https://developers.yubico.com/yubikey-val/Validation_Protocol_V2.0.html). Yubikey devices and server API keys can easily be managed in the Django admin site.\n\n\n## Installation\n\nYubival can be integrated to any existing Django project. Alternatively, you can create a new Django site to host your validation server. If unfamiliar with Django, please follow the instructions at "Create a new standalone validation server" below.\n\n\n### Add Yubival to an existing Django project\n\nInstall the package from PyPI:\n\n```\n$ pip install yubival\n```\n\nAdd `\'yubival\'` to the `INSTALLED_APPS` setting in settings.py. Since it is recommended to also enable the admin site, `INSTALLED_APPS` may look like:\n\n```\nINSTALLED_APPS = [\n    \'django.contrib.admin\',\n    \'django.contrib.auth\',\n    \'django.contrib.contenttypes\',\n    \'django.contrib.sessions\',\n    \'django.contrib.messages\',\n    \'django.contrib.staticfiles\',\n    \'yubival\',\n]\n```\n\nAdd the app URLs to the root urls.py file:\n\n```\nfrom django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    # ...\n    path(\'admin/\', admin.site.urls),\n    path(\'\', include(\'yubival.urls\')),\n]\n```\n\nUpdate the database:\n\n```\npython manage.py migrate\n```\n\nWhen running the server, you should now be able to query the API at `/wsapi/2.0/verify`. When not providing any GET parameters, this returns a `MISSING_PARAMETER` status:\n\n```\nt=2021-10-29T08:31:11.885803\nstatus=MISSING_PARAMETER\n```\n\n\n### Create a new standalone validation server\n\nThis section explains how to setup a new Django site with Yubival. It was tested on a Debian 10 distribution, with Python 3.9 and Django 3.2.\n\nCreate a directory for the project:\n\n```\n$ mkdir myyubival\n$ cd myyubival\n```\n\nCreate a Python environment and activate it:\n\n```\n$ python3 -m venv venv\n$ source venv/bin/activate\n```\n\nInstall Django and Yubival:\n\n```\n$ pip install Django yubival\n```\n\nCreate a new Django project and browse to the newly created directory:\n\n```\n$ django-admin startproject myyubival\n$ cd myyubival\n```\n\nEdit the _./myyubival/settings.py_ file to add `\'yubival\'` to the `INSTALLED_APPS` setting:\n\n```\nINSTALLED_APPS = [\n    # ...\n    \'yubival\',\n]\n```\n\nMake the validation server URLs accessible by editing _./myyubival/urls.py_. Include the URLs from the Yubival app:\n\n```\nfrom django.contrib import admin\nfrom django.urls import path, include\nfrom django.views.generic.base import RedirectView\n\nurlpatterns = [\n    path(\'\', RedirectView.as_view(pattern_name=\'admin:index\')),\n    path(\'admin/\', admin.site.urls),\n    path(\'\', include(\'yubival.urls\')),\n]\n```\n\nFor convenience, we redirect above the website root to the admin area.\n\nBy default, Django will create a SQLite database located in a _db.sqlite3_ file in the project directory. To use other database engines, edit _./myyubival/settings.py_ to change the `DATABASES` setting; see the [Databases doc](https://docs.djangoproject.com/en/dev/ref/databases/). In both cases, run afterwards the following command to create the initial database tables:\n\n```\npython manage.py migrate\n```\n\nTo be able to use the admin site and manage Yubikey devices and server API keys, create an initial user account:\n\n```\n$ python manage.py createsuperuser\n```\n\nTo run the development web server, launch:\n\n```\n$ python manage.py runserver\n```\n\nThe website can now be accessed at http://127.0.0.1:8000/. It should show a "Page not found" error. The validation API is located at http://127.0.0.1:8000/wsapi/2.0/verify and the admin site interface at http://127.0.0.1:8000/admin/.\n\nWhile the `runserver` command above is an easy way to check your configuration and test Yubival, it should not be used to run the web server in production. Refer to the [deployment docs](https://docs.djangoproject.com/en/dev/howto/deployment/) to learn how to deploy your new myyubival site.\n',
    'author': 'Nicolas Bruot',
    'author_email': 'coremeltdown@bruot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bruot/yubival',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
