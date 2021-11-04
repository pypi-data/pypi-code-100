# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csc_recorder']

package_data = \
{'': ['*'], 'csc_recorder': ['CSC/templates/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0', 'requests>=2.26.0,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'csc-recorder',
    'version': '1.3.0',
    'description': 'CSC eRecording python wrapper',
    'long_description': "# csc-recorder\n\nPython wrapper for CSC Recorder.\n\n`pip install csc-recorder`\n\n\n## Usuage\n\n```\nfrom csc_recorder.CSCRecorder import CSCRecorder\n\n\nclient = CSCRecorder('host', 'username', 'password')\n\n# Sending a package\ndata, response = client.send_package('1234_TEST', '48201', 'Default Office', {'document_name': 'test', 'document_type': 'Deed'}, 'paperfulfillment', True)\n\n```\nThe first three params are required:\n- client_package_id\n- fips\n- assigned_office\n\nThe dictionary in the params supports the below attributes, they're not required:\n- document_name\n- document_type\n- send_to_county\n- send_to_state\n- grantee_first_name\n- grantee_last_name\n- grantee_middle_name\n- grantee_suffix\n- grantee_title\n- grantor_first_name\n- grantor_first_name\n- grantor_last_name\n- grantor_middle_name\n- grantor_suffix\n- grantor_title\n- consideration_amount\n- original_recording_date\n- original_instrument_no\n- original_deed_book\n- original_deed_page\n- assesors_parcel_id\n- date_of_note\n- amount_of_note\n- property_street_address_1\n- property_city\n- property_state\n- property_zip\n- requesting_name\n- return_name\n- return_company\n- return_street_address_1\n- return_city\n- return_state\n- return_zip\n- requesting_company\n- requesting_address_1\n- requesting_city\n- requesting_state\n- requesting_zip\n- doc_image **(NOTE: base64 PDF's)\n\nThe last 2 params are optional as well.\n- service_type, defaults to None, but currently you can also add 'paperfulillment'\n- no_document, defaults to False, but you can make the package send 0 document attributes by marking True",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/CSCRecorder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
