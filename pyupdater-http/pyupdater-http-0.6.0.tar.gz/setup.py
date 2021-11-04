# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyupdater_http']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

entry_points = \
{'pyupdater.plugins': ['http_uploader = pyupdater_http.uploader:HTTPUploader']}

setup_kwargs = {
    'name': 'pyupdater-http',
    'version': '0.6.0',
    'description': 'PyUpdater Plugin: HTTP upload support',
    'long_description': '[![Build Status](https://img.shields.io/github/workflow/status/micro-fan/pyupdater-http/main)](https://github.com/micro-fan/pyupdater-http/actions)\n[![PyPi version](https://img.shields.io/pypi/v/pyupdater-http.svg)](https://pypi.python.org/pypi/pyupdater-http)\n\n\n## Parameters\n\n* `server_url` - add basic auth if you need it\n* `data_params` - additional params that will be passed with file\n* `filename_param` - field name for file name if your server need it\n\n\n## Usage Example\n\n### with `codeskyblue/gohttpserver`\n\n\nTraefik is optional, you can export direct ports. This is just reminder of how we\'re doing it\n\n```bash\n$ pip install --user -U dot-tools\n$ exec zsh\n\n# if you have local packages in your `PATH`\n# like: `/home/user/.local/bin/traefik_run`\n\n$ traefik_run up -d\n```\n\nThen launch your web site\n\n```yaml\nversion: \'3.9\'\n\nservices:\n  releases_server:\n    image: codeskyblue/gohttpserver:1.1.0\n    container_name: releases_server\n    # define only if you want to have basic-auth\n    command: --auth-type http --auth-http basic_auth_user:basic_auth_password\n    volumes:\n      - ./uploads:/app/public\n    # you can export ports if you\'re not using traefik\n    labels:\n      - "traefik.enable=true"\n      - "traefik.http.routers.releases.rule=Host(`releases.example.com`)"\n      - "traefik.http.routers.releases.entrypoints=web"\n\n```\n\nAnd put into `uploads` directory file `.ghs.yaml`:\n\n```yaml\n---\nupload: false\ndelete: false\nusers:\n- email: "cybergrind@example.com"\n  delete: true\n  upload: true\n  token: auth_token_for_upload\n```\n\nAnd add configuration in your `config.pyu`\n\n```json\n{\n "app_config": {\n    "PLUGIN_CONFIGS": {\n      "httpuploader-@cybergrind": {\n        "server_url": "http://basic_auth_user:basic_auth_password@releases.example.com/",\n        "data_params": {\n          "token": "auth_token_for_upload"\n        },\n        "timeout": 600,\n        "filename_param": "filename"\n      }\n    }\n  }\n}\n```\n',
    'author': 'Kirill Pinchuk',
    'author_email': 'cybergrind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/micro-fan/pyupdater-http',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
