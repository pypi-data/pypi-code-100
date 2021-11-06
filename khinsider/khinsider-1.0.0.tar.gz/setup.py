# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['khinsider']
install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['khinsider = khinsider:main']}

setup_kwargs = {
    'name': 'khinsider',
    'version': '1.0.0',
    'description': 'A script for khinsider mass downloads. Get video game soundtracks quickly and easily! Also a Python interface.',
    'long_description': '# khinsider.py\n\n> This is a modified version of khinisder.py with an\n> explicit focus of being easy to upload to and install\n> from PyPI. Please go support the original release:\n> https://github.com/obskyr/khinsider\n\n`khinsider.py` is a [Python](https://www.python.org/) interface for getting [khinsider](http://downloads.khinsider.com/) soundtracks. It makes khinsider mass downloads a breeze. It\'s easy to use - check it!\n\nFrom the command line:\n\n```cmd\nkhinsider.py jumping-flash\n```\n\nAs an import:\n\n```python\nimport khinsider\nkhinsider.download(\'jumping-flash\')\n# And bam, you\'ve got the Jumping Flash soundtrack!\n```\n\nFor anime music, [check out `thehylia.py`](https://github.com/obskyr/thehylia).\n\nCarefully put together by [@obskyr](http://twitter.com/obskyr)!\n\n### **[Download it here!](https://github.com/obskyr/khinsider/archive/master.zip)**\n\n## Usage\n\nJust run `khinsider.py` from the command line with the sole parameter being the soundtrack you want to download. You can either use the soundtrack\'s ID, or simply copy its entire URL. Easy!\n\nIf you want, you can also add another parameter as the output folder, but that\'s optional.\n\nYou can also download other file formats (if available), like FLAC or OGG, as following:\n\n```cmd\nkhinsider.py --format flac mother-3\n```\n\nIf you don\'t want to go to the actual site to look for soundtracks, you can also just type a search term as the first parameter(s), and provided it\'s not a valid soundtrack, `khinsider.py` will give you a list of soundtracks matching that term.\n\nYou\'re going to need [Python](https://www.python.org/downloads/) (if you don\'t know which version to get, choose the latest version of Python 3 - `khinsider.py` works with both 2 and 3), so install that (and [add it to your path](http://superuser.com/a/143121)) if you haven\'t already.\n\nYou will also need to have [pip](https://pip.readthedocs.org/en/latest/installing.html) installed (if you have Python 3, it is most likely already installed - otherwise, download `get-pip.py` and run it) if you don\'t already have [requests](https://pypi.python.org/pypi/requests) and [Beautiful Soup 4](https://pypi.python.org/pypi/beautifulsoup4). The first time `khinsider.py` runs, it will install these two for you.\n\nFor more detailed information, try running `khinsider.py --help`!\n\n## As a module\n\n`khinsider.py` requires two non-standard modules: [requests](https://pypi.python.org/pypi/requests) and [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4). Just run a `pip install` on them (with [pip](https://pip.readthedocs.org/en/latest/installing.html)), or just run `khinsider.py` on its own once and it\'ll install them for you.\n\nHere are the main functions you will be using:\n\n### `khinsider.download(soundtrackName[, path="", makeDirs=True, formatOrder=None, verbose=False])`\n\nDownload the soundtrack `soundtrackName`. This should be the name the soundtrack uses at the end of its album URL.\n\nIf `path` is specified, the soundtrack files will be downloaded to the directory that path points to.\n\nIf `makeDirs` is `True`, the directory will be created if it doesn\'t exist.\n\nYou can specify `formatOrder` to download soundtracks in specific formats. `formatOrder=[\'flac\', \'mp3\']`, for example, will download FLACs if available, and MP3s if not.\n\nIf `verbose` is `True`, it will print progress as it is downloading.\n\n### `khinsider.search(term)`\n\nSearch khinsider for `term`. Return a list of `Soundtrack`s matching the search term. You can then access `soundtrack.id` or `soundtrack.url`.\n\n### More\n\nThere\'s a lot more detail to the API - more than would be sensible to write here. If you want to use `khinsider.py` as a module in a more advanced capacity, have a look at the `Soundtrack`, `Song`, and `File` objects in the source code! They\'re documented properly there for your reading pleasure.\n\n# Talk to me!\n\nYou can easily get to me in these ways:\n\n* [@obskyr](http://twitter.com/obskyr/) on Twitter!\n* [E-mail](mailto:powpowd@gmail.com) me!\n\nI\'d love to hear it if you like `khinsider.py`! If there\'s a problem, or you\'d like a new feature, submit an issue here on GitHub.\n',
    'author': 'Kyle Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SuperSonicHub1/khinsider',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
