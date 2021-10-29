# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['innertube']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.4.0,<3.0.0',
 'agency>=0.1.1,<0.2.0',
 'attrs>=21.2.0,<22.0.0',
 'enumb>=0.1.2,<0.2.0',
 'furl>=2.1.0,<3.0.0',
 'mimit>=0.1.4,<0.2.0',
 'parse>=1.19.0,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'registrate>=0.1.2,<0.2.0',
 'requests>=2.25.1,<3.0.0',
 'soset>=0.1.0,<0.2.0',
 'toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'innertube',
    'version': '1.0.4',
    'description': "Python Client for Google's Private InnerTube API. Works with Youtube, YouTubeMusic etc.",
    'long_description': "# innertube\nPython Client for Google's Private InnerTube API. Works with: **YouTube**, **YouTube Music**, **YouTube Kids**, **YouTube Studio**\n\n## About\nThis library handles low-level interactions with the InnerTube API that is used by each of the YouTube services.\nGoogle hasn't made much public about the API, and recently all App interactions use [protobuf](https://github.com/protocolbuffers/protobuf) making them hard to reverse-engineer. The only articles I could find online are:\n* [Gizmodo - How Project InnerTube Helped Pull YouTube Out of the Gutter](https://gizmodo.com/how-project-innertube-helped-pull-youtube-out-of-the-gu-1704946491)\n* [Fast Company - To Take On HBO And Netflix, YouTube Had To Rewire Itself](https://www.fastcompany.com/3044995/to-take-on-hbo-and-netflix-youtube-had-to-rewire-itself)\n\n## Installation\nThe `innertube` library uses [Poetry](https://github.com/python-poetry/poetry) and can easily be installed from source, or using *pip*\n\n### Using *pip* (from source)\n```console\n$ pip install git+https://github.com/tombulled/innertube\n```\n\n## Usage\n```python\n>>> import innertube\n>>>\n>>> # Construct a client\n>>> client = innertube.InnerTube(innertube.Client.WEB)\n>>>\n>>> # Get some data!\n>>> data = client.search(query = 'foo fighters')\n>>>\n>>> # Power user? No problem, dispatch requests yourself\n>>> data = client('browse', json = {'browseId': 'FEwhat_to_watch'})\n>>>\n>>> # The core endpoints are implemented, so the above is equivalent to:\n>>> data = client.browse('FEwhat_to_watch')\n```\n\n## Why not just use the [YouTube Data API](https://developers.google.com/youtube/v3/)?\nIt's entirely up to you and your needs, however this library provides functionality you wont get from the Data API, but it comes at somewhat of a cost *(explained below)*\n|                                       | This Library | YouTube Data API |\n| ------------------------------------- | ------------ | ---------------- |\n| No Google account required            | &check;      | &cross;          |\n| No request limit                      | &check;      | &cross;          |\n| Clean, reliable, well-structured data | &cross;      | &check;          |\n\n### Wait a sec! What do you mean it's not clean, reliable and well-structured??\nWell, the private InnerTube API is not designed for consumption by users, it is used to render and operate the various YouTube services.\n\n### What does that mean?\nSimply put, the data returned by the InnerTube API will need to be parsed and sanitised to extract the usable data as it will contain a lot of fluff that is unlikely to be of any use. These higher-level clients are in the works!\n\n## Clients\nThis table shows all the devices and services that work with the InnerTube API. For example, you could query the API as if you were using the YouTube app on your Tv!\n|         | YouTube | YouTubeMusic  | YouTubeKids  | YouTubeStudio   |\n| ------- | ------- | ------------- | ------------ | --------------- |\n| Web     | WEB     | WEB_REMIX     | WEB_KIDS     | WEB_CREATOR     |\n| Android | ANDROID | ANDROID_MUSIC | ANDROID_KIDS | ANDROID_CREATOR |\n| Ios     | IOS     | IOS_MUSIC     | IOS_KIDS     | IOS_CREATOR     |\n| Tv      | TVHTML5 |               |              |                 |\n\n## Endpoints\nOnly the core, unauthenticated endpoints are currently implemented. However, between all of these you should be able to access all the data you need.\n|                                | YouTube | YouTubeMusic | YouTubeKids | YouTubeStudio |\n| ------------------------------ | ------- | ------------ | ----------- | ------------- |\n| config                         | &check; | &check;      | &check;     | &check;       |\n| browse                         | &check; | &check;      | &check;     | &check;       |\n| player                         | &check; | &check;      | &check;     | &check;       |\n| next                           | &check; | &check;      | &check;     | &cross;       |\n| search                         | &check; | &check;      | &check;     | &cross;       |\n| guide                          | &check; | &check;      | &cross;     | &cross;       |\n| music/get_search_suggestions   | &cross; | &check;      | &cross;     | &cross;       |\n| music/get_queue                | &cross; | &check;      | &cross;     | &cross;       |\n\n## What about Authentication?\nThe InnerTube API uses OAuth2, however I have been unable to successfully implement authentication.\nTherefore, this library currently only provides unauthenticated access to the API.\n\n## Credits\nHere's a list of the awesome libraries that helped make `innertube`\n| PyPi | Source |\n| ---- | ------ |\n| [requests](https://pypi.org/project/requests/) | https://github.com/psf/requests |\n| [pydantic](https://pypi.org/project/pydantic/) | https://github.com/samuelcolvin/pydantic |\n| [addict](https://pypi.org/project/addict/) | https://github.com/mewwts/addict |\n| [attrs](https://pypi.org/project/attrs/) | https://github.com/python-attrs/attrs |\n| [furl](https://pypi.org/project/furl/) | https://github.com/gruns/furl |\n| [humps](https://pypi.org/project/pyhumps/) | https://github.com/nficano/humps |\n| [parse](https://pypi.org/project/parse/) | https://github.com/r1chardj0n3s/parse |\n| [toolz](https://pypi.org/project/toolz/) | https://github.com/pytoolz/toolz |\n",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/innertube',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
