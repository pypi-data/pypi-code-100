# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sadales_tikls_m2m_api_client',
 'sadales_tikls_m2m_api_client.api',
 'sadales_tikls_m2m_api_client.api.default',
 'sadales_tikls_m2m_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'httpx>=0.15.4,<0.20.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'sadales-tikls-m2m',
    'version': '1.0.0',
    'description': 'A client library for accessing Sadales Tikls M2M API',
    'long_description': '# sadales-tikls-m2m-api-client\nA client library for accessing Sadales Tikls M2M API\n\n## OpenAPI\nSee preview in [Swagger Editor online](https://editor.swagger.io/?url=https://raw.githubusercontent.com/vermut/sadales-tikls-m2m/master/openapi.yaml).\n\n> Keep in mind that direct queries from browser won\'t work due to known CORS issue.\n\n## Usage\nFirst, create a client:\n\n```python\nfrom sadales_tikls_m2m_api_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://services.e-st.lv/m2m", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom sadales_tikls_m2m_api_client import AuthenticatedClient\nfrom sadales_tikls_m2m_api_client.types import Response\nfrom sadales_tikls_m2m_api_client.api.default import get_object_list\nfrom sadales_tikls_m2m_api_client.models import GetObjectListResponse200\n\nobjects: GetObjectListResponse200 = get_object_list.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[GetObjectListResponse200] = get_object_list.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom sadales_tikls_m2m_api_client import AuthenticatedClient\nfrom sadales_tikls_m2m_api_client.types import Response\nfrom sadales_tikls_m2m_api_client.api.default import get_object_list\nfrom sadales_tikls_m2m_api_client.models import GetObjectListResponse200\n\nmy_data: GetObjectListResponse200 = await get_object_list.asyncio(client=client)\nresponse: Response[GetObjectListResponse200] = await get_object_list.asyncio_detailed(client=client)\n```\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but the async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `sadales_tikls_m2m_api_client.api.default`\n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`\n',
    'author': 'Pavels Veretennikovs',
    'author_email': 'vermut@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vermut/sadales-tikls-m2m',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
