# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qsl', 'qsl.testing', 'qsl.types']

package_data = \
{'': ['*'],
 'qsl': ['frontend/*',
         'frontend/static/css/*',
         'frontend/static/js/*',
         'frontend/static/media/*'],
 'qsl.testing': ['data/*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'aiofiles',
 'async-exit-stack>=1.0.1,<2.0.0',
 'async_generator>=1.10,<2.0',
 'boto3>=1.17.15,<2.0.0',
 'click',
 'fastapi',
 'filetype>=1.0.7,<2.0.0',
 'httpx>=0.19.0,<0.20.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'uvicorn[standard]>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['qsl = qsl.cli:cli']}

setup_kwargs = {
    'name': 'qsl',
    'version': '0.0.30',
    'description': 'Yet another data labeling tool',
    'long_description': '# QSL: Quick and Simple Labeler\n\n![QSL Screenshot](https://raw.githubusercontent.com/faustomorales/qsl/main/docs/screenshot.png)\n\n\nQSL is a simple, open-source image labeling tool. It supports:\n\n- Bounding box and polygon labeling.\n- Configurable keyboard shortcuts for labels.\n- Loading images stored locally, on the web, or in cloud storage (currently only AWS S3).\n- Pre-loading images in a queue to speed up labeling.\n- Deployment as shared service with support for OAuth (currently only GitHub and Google)\n\nPlease note that that QSL is still under development and there are likely to be major bugs, breaking changes, etc. Bug reports and contributions are welcome!\n\n## Getting Started\n\nInstall `qsl` using `pip install qsl`. _You cannot install `qsl` directly from the GitHub repository because the frontend assets must be built manually._\n\nYou can start a simple project labeling files from your machine using a command like the following.\n\n```bash\nqsl simple-label path/to/files/*.jpg my-qsl-project.json\n```\n\nNote that if `my-qsl-project.json` already exists and has files in it, these files will be added (the old files will still be in the project). If it does not exist, an empty project file will be created.\n\nYou can navigate to the the QSL labeling interface in a browser at `http://localhost:5000` (use the `--host` and `--port` flags to modify this). From the interface, click the link to `Configure project` to set which labels you want to apply to images. Labels can be applied at the `image` or `box` level. There are three kinds of labels you can use:\n\n- _Single_: You select 0 or 1 entry from a list of options.\n- _Multiple_: You select 0 or more entries from a list of options.\n- _Text_: A free-form text field.\n\nAfter configuring the project, you can immediately start labeling single images from the main project page. When you\'re done (or just want to pause) hit Ctrl+C at the prompt where you started QSL. The labels will be available in `my-qsl-project.json`. You can parse this yourself pretty easily, but you can also save yourself the trouble by using the data structures within QSL. For example, the following will load the image- and box-level labels for a project into a `pandas` dataframe.\n\n```python\nimport pandas as pd\nimport qsl.types.web as qtw\n\nwith open("my-qsl-project.json", "r") as f:\n    project = qtw.Project.parse_raw(f.read())\n\nimage_level_labels = pd.DataFrame(project.image_level_labels())\nbox_level_labels = pd.DataFrame(project.box_level_labels())\n```\n\n### Labeling Remotely Hosted Files\n\nNote that QSL also supports labeling files hosted remotely in cloud storage (only AWS S3 is supported right now) or at a public URL. So, for example, if you want to label some files in an S3 bucket and on a web site, you can use the following command:\n\n```bash\nqsl simple-label \'s3://my-bucket/images/*.jpg\' \'s3://my-bucket/other/*.jpg\' \'http://my-site/image.jpg\' my-qsl-project.json\n```\n\nPlease note that paths like this must meet some criteria.\n\n- On most platforms / shells, you must use quotes (as shown in the example).\n- Your AWS credentials must be available in a form compatible with the default `boto3` credential-finding methods and those credentials must be permitted to use the `ListBucket` and `GetObject` actions.\n\n### Advanced Use Cases\nDocumentation for the more advanced use cases is not yet available though they are implemented in the package. Advanced use cases include things like:\n\n- Hosting a central QSL server with multiple users and projects\n- Authentication with Google or GitHub OAuth providers\n- Batched labeling for images with shared default labels\n\nIn short, you can launch a full-blown QSL deployment simply by doing the following.\n\n1. Set the following environment variables to configure the application.\n    - `DB_CONNECTION_STRING`: A database connection string, used to host the application data. If not provided, a SQLite database will be used in the current working directory called `qsl-labeling.db`.\n    - `OAUTH_INITIAL_USER`: The initial user that will be an administrator for the QSL instance.\n    - `OAUTH_PROVIDER`: The OAuth provider to use (currently `github` and `google` are supported)\n    - `OAUTH_CLIENT_SECRET`: The OAuth client secret.\n    - `OAUTH_CLIENT_ID`: The OAuth client ID.\n2. Execute `qsl label` (instead of `qsl simple-label`) to launch the application (use `--host` and `--port` to modify how the application listens for connections).\n\n\n# Development\n\n1. Install Poetry.\n2. Clone this repository.\n3. Initialize your development environment using `make init`\n4. Launch a live reloading version of the frontend and backend using `make develop`.\n',
    'author': 'Fausto Morales',
    'author_email': 'faustomorales@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faustomorales/qsl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
