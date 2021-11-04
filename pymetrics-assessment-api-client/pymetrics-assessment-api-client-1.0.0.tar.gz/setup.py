# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymetrics_assessment_api_client',
 'pymetrics_assessment_api_client.api',
 'pymetrics_assessment_api_client.api.default',
 'pymetrics_assessment_api_client.examples',
 'pymetrics_assessment_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'httpx>=0.15.4,<0.21.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'pymetrics-assessment-api-client',
    'version': '1.0.0',
    'description': 'A client library for accessing pymetrics Assessment API',
    'long_description': '# pymetrics-assessment-api-client\nA client library for accessing pymetrics Assessment API\n\n## Installation\n\n```bash\npip install pymetrics-assessment-api-client\n```\n\n## Usage\n\nA full set of examples can be found in the [pymetrics-assessments-api-client examples directory](https://github.com/pymetrics/pymetrics_assessment_api_client/tree/main/pymetrics_assessment_api_client/examples).\n\nTo get started, please request Client ID, Client Secret and API Key from pymetrics.\n\nFirst, create a client for staging environment:\n\n```python\nfrom pymetrics_assessment_api_client import Client\n\nclient = Client(base_url="https://staging.pymetrics.com")\n```\n\nTo get an authenticated token, you can hit the get oauth endpoint by doing the following:\n```python\nfrom pymetrics_assessment_api_client.models import OAuthTokenRequest\nfrom pymetrics_assessment_api_client.api.default import mercury_o_auth\nfrom pymetrics_assessment_api_client.models import OAuthTokenResponse\nfrom pymetrics_assessment_api_client.types import Response\n\nrequest = OAuthTokenRequest(client_id=client_id,\n                            client_secret=client_secret,\n                            grant_type="client_credentials")\nauth_response: Response = mercury_o_auth.sync_detailed(client=client,\n                                                       json_body=request)\nauth_token_response: OAuthTokenResponse = auth_response.parsed\nprint(f"Access Token: {auth_token_response.access_token}")\n```\nTo retrieve an order, you can use the token generated above and hit the get order endpoint:\n```python\nfrom pymetrics_assessment_api_client.api.default import mercury_retrieve_order\nfrom pymetrics_assessment_api_client.models import MercuryAssessmentOrder\nfrom pymetrics_assessment_api_client.types import Response\n\nauth = f"Bearer {access_token}"\n\nget_order_response: Response = mercury_retrieve_order.sync_detailed(\n    client=client,\n    uuid=order_uuid,\n    authorization=auth,\n    x_api_key=API_KEY,\n    report=False\n)\nparsed_get_order_response: MercuryAssessmentOrder = get_order_response.parsed\nprint(f"Successfully retrieved order: {parsed_get_order_response.to_dict()}")\n```\n\n## Base URLs\nUS Production: https://www.pymetrics.com\n\nUS Staging: https://staging.pymetrics.com',
    'author': 'Michelle Tsai',
    'author_email': 'min.tsai@pymetrics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
