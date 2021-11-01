# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvc_flask']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'mvc-flask',
    'version': '2.0.0',
    'description': 'turn standard flask into mvc',
    'long_description': '![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/marcuxyz/mvc_flask) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/marcuxyz/mvc_flask/unit%20test) ![GitHub](https://img.shields.io/github/license/marcuxyz/mvc_flask) ![PyPI - Downloads](https://img.shields.io/pypi/dm/mvc_flask) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mvc_flask) ![PyPI](https://img.shields.io/pypi/v/mvc_flask)\n\nYou can use the mvc pattern in your flask application using this extension.\n\n## Installation\n\nRun the follow command to install `mvc_flask`:\n\n```shell\n$ pip install mvc_flask\n```\n\n## Configuration\n\nTo configure the `mvc_flask` you need import and register in your application, e.g:\n\n\n```python\nfrom flask import Flask\nfrom mvc_flask import FlaskMVC\n\napp = Flask(__name__)\nFlaskMVC(app)\n```\n\nOr use `application factories`, e.g:\n\n```python\nmvc = FlaskMVC()\n\ndef create_app():\n  ...\n  mvc.init_app(app)\n```\n\n**By default the `mvc_flask` assumes that your application directory will be `app` and if it doesn\'t exist, create it!**\n\nYou structure should be look like this: \n\n```text\napp\n├── __ini__.py\n├── controllers\n│   └── home_controller.py\n├── routes.py\n└── views\n    ├── index.html\n```\n\n## Router\nYou can create routes in `app/routes.py` and after create file, you can start register routes, e.g:\n\n```python\nfrom mvc_flask import Router\n\nRouter.get("/", "home#index")\n```\n\nThe same must be make done to `POST`, `PUT` and `DELETE` methods. E.g: `Router.post("/messages", "messages#create")`\n\nThe first param represent the relative path and second represent the `controller#action`. Remember that we are working with `MVC pattern`, so we have `controller` and `action`.\n\nThe `controller` can be created in `app/controllers` and action is method of `controller`.\n\n## Controller\n\nNow that configure routes, the `home_controller.py` file must contain the `HomeController` class, registering the `action`, e.g:  \n\n```python\nfrom flask import render_template\n\nclass HomeController:\n    def index(self):\n        return render_template("index.html")\n```\n\nIf you have question, please, check de [app](https://github.com/marcuxyz/mvc_flask/tree/main/app) directory to more details.\n\n# Tests\n\nYou can run the tests, executing the follow command:\n\n```shell\n$ make test\n```\n',
    'author': 'Marcus Pereira',
    'author_email': 'oi@negros.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcuxyz/mvc_flask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
