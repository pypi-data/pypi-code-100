# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apiman']

package_data = \
{'': ['*'], 'apiman': ['static/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0', 'PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'apiman',
    'version': '0.2.4',
    'description': 'Integrate api manual for your web project',
    'long_description': '# APIMAN\n\n[![Build](https://travis-ci.com/strongbugman/apiman.svg?branch=master)](https://travis-ci.com/strongbugman/apiman)\n[![codecov](https://codecov.io/gh/strongbugman/apiman/branch/master/graph/badge.svg)](https://codecov.io/gh/strongbugman/apiman)\n\nAPIMAN provide a easy way to integrate api manual/document for your web project\n\n## Features\n\n* Support OpenAPI 2 and 3 specification, define API specification by file or doc\n* Provide configurable [SwaggerUI](http://swagger.io/swagger-ui/) and [RedocUI](https://rebilly.github.io/ReDoc/)\n* Outbox extension for flask and Starlette\n\n## Install\n\n```shell\npip install -U apiman\n```\n\n## Examples\n\nLet\'s see a Starlette example app:\n\n```python\n"""OpenAPI2(Swagger) with Starlette\n"""\nfrom starlette.applications import Starlette\nfrom starlette.requests import Request\nfrom starlette.responses import JSONResponse\nfrom starlette.endpoints import HTTPEndpoint\nfrom uvicorn import run\nfrom openapi_spec_validator import validate_v2_spec\nfrom starlette.testclient import TestClient\n\nfrom apiman.starlette import Extension\n\n\napp = Starlette()\nopenapi = Extension(template="./examples/docs/cat_template.yml")\nopenapi.init_app(app)\n\n\n# define data\nCATS = {\n    1: {"id": 1, "name": "DangDang", "age": 2},\n    2: {"id": 2, "name": "DingDing", "age": 1},\n}\n# add schema definition\nopenapi.add_schema(\n    "Cat",\n    {\n        "properties": {\n            "id": {"description": "global unique", "type": "integer"},\n            "name": {"type": "string"},\n            "age": {"type": "integer"},\n        },\n        "type": "object",\n    },\n)\n\n\n# define routes and schema(in doc string)\n@app.route("/cat/")\nclass Cat(HTTPEndpoint):\n    """\n    Declare multi method\n    ---\n    get:\n      summary: Get single cat\n      tags:\n      - cat\n      parameters:\n      - name: id\n        type: integer\n        in: path\n        required: True\n      responses:\n        "200":\n          description: OK\n          schema:\n            $ref: \'#/definitions/Cat\'\n        "404":\n          description: Not found\n    """\n\n    def get(self, req: Request):\n        return JSONResponse(CATS[int(req.path_params["id"])])\n\n    def delete(self, req: Request):\n        """\n        Declare single method\n        ---\n        summary: Delete single cat\n        tags:\n        - cat\n        parameters:\n        - name: id\n          type: integer\n          in: path\n          required: True\n        responses:\n          "204":\n            description: OK\n            schema:\n              $ref: \'#/definitions/Cat\'\n          "404":\n            description: Not found\n        """\n        cat = CATS.pop(int(req.path_params["id"]))\n        return JSONResponse(cat)\n\n\n# define doc by yaml or json file\n@app.route("/cats/", methods=["GET"])\n@openapi.from_file("./examples/docs/cats_get.yml")\ndef list_cats(req: Request):\n    return JSONResponse(list(CATS.values()))\n\n\n@app.route("/cats/", methods=["POST"])\n@openapi.from_file("./examples/docs/cats_post.json")\nasync def list_cats(req: Request):\n    cat = await req.json()\n    CATS[cat["id"]] = cat\n    return JSONResponse(cat)\n\n\nif __name__ == "__main__":\n    run(app)\n```\n\nThen we can get swagger web page at [http://localhost:8000/apiman/swagger/](http://localhost:8000/apiman/swagger/):\n![WebPage](docs/SwaggerUI.jpg)\n\nSee **examples/** for more examples\n\n## How it works\n\n* Provide a base class("OpenApi") to handle api specification\'s collection\n* Provide extentions to extract api specification and register http endpoints to show UI web page and specification\n',
    'author': 'strongbugman',
    'author_email': 'strongbugman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/strongbugman/ant_nest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
