# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.pelican_algolia']

package_data = \
{'': ['*']}

install_requires = \
['algoliasearch>=2.6.0', 'pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-algolia',
    'version': '1.0.0',
    'description': 'Plugin to integrate Algolia Search with Pelican SSG',
    'long_description': 'Algolia Search: A Plugin for Pelican\n====================================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/rehanhaider/pelican-algolia/build)](https://github.com/rehanhaider/pelican-algolia/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-algolia)](https://pypi.org/project/pelican-algolia/)\n![License](https://img.shields.io/pypi/l/pelican-algolia?color=blue)\n\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-algolia\n\nPrerequisites\n-------------\n1. Create an [Algolia](https://www.algolia.com/) account\n2. On Algolia website, create a new application\n3. Create a new Index (or Indices) in you Algolia app. This will be `ALGOLIA_INDEX_NAME`\n4. Import you records, if asked select **Use the API** option\n5. Go to Settings -> API Keys -> Your API Keys and copy your \n    * Application ID, this will be `ALGOLIA_APP_ID`\n    * Admin API Key (**DO NOT HARD CODE THIS IN YOUR PROGRAM**). This will be `ALGOLIA_ADMIN_API_KEY`\n    * Algolia Search-Only API Key. This will be `ALGOLIA_SEARCH_API_KEY`\n\nUsage\n-----\n**Step 1**: Set the following configuration in `pelicanconf.py`\n```python\n# Algolia Publish Data\nALGOLIA_APP_ID = "<Your Algolia App ID>"\nALGOLIA_SEARCH_API_KEY = "<Your Search-only Api Key>"\nALGOLIA_INDEX_NAME = "<You Algolia App Index name>"\n```\n**Step 2**: Set the `ALGOLIA_ADMIN_API_KEY` as an environmatal variable on path\n\n**Step 3**: Import `ALGOLIA_ADMIN_API_KEY` in your `publishconf.py` (or `pelicanconf.py` if you\'re not using `publishconf.py` for publish settings)\n```python\nimport os\nALGOLIA_ADMIN_API_KEY = os.environ.get("ALGOLIA_ADMIN_API_KEY")\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/rehanhaider/pelican-algolia/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Rehan Haider',
    'author_email': 'email@rehanhaider.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rehanhaider/pelican-algolia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
