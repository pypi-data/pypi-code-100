# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdownio']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'markdownio',
    'version': '0.1.0',
    'description': 'Python tool to write Markdown as code easily.',
    'long_description': '# MarkdownIO\n\n[![Pypi Version](https://img.shields.io/pypi/v/markdownio.svg)](https://pypi.org/project/markdownio/)\n[![Python Version](https://img.shields.io/pypi/pyversions/markdownio)](https://pypi.org/project/markdownio/)\n[![CI](https://github.com/u8slvn/markdownio/actions/workflows/ci.yml/badge.svg)](https://github.com/u8slvn/markdownio/actions/workflows/ci.yml)\n[![Coverage Status](https://coveralls.io/repos/github/u8slvn/markdownio/badge.svg?branch=master)](https://coveralls.io/github/u8slvn/markdownio?branch=master)\n[![Project license](https://img.shields.io/pypi/l/markdownio)](https://pypi.org/project/markdownio/)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython tool to write Markdown as code easily.\n\n## Installation\n\n```sh\n$ pip install markdownio\n```\n\n## Usage\n\n```python\nfrom markdownio import MarkdownIO, span\nfrom markdownio.block import TableHeader\n\nmarkdown = MarkdownIO()\n\nmarkdown.h1("My test document")\nmarkdown.p(\n    text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. "\n         "Vivamus rutrum consequat " + span.bold("odio") + " et mollis."\n)\nmarkdown.p(span.image(path="path/img.jpg", alt="img", title="img"))\nmarkdown.table(\n    columns=3,\n    headers=[\'Col1\', \'Col2\', TableHeader.center(\'Col3\')],\n    rows=[\n        [\'foo\', \'bar\', \'foobar\'],\n        [\'oof\', \'rab\', 2000],\n    ]\n)\nmarkdown.p(\n    text="This is an interesting article: " + span.link(path=\'http://test.io\')\n)\nmarkdown.h2("Code example")\nmarkdown.code(text=\'<p>Test</p>\', language=\'html\')\n\nprint(markdown.output())\n```\n\noutput:\n\n~~~markdown\n# My test document\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus rutrum consequat **odio** et mollis. p\n![img](path/img.jpg "img")\n\n| Col1 | Col2 | Col3   |\n| ---- | ---- | :----: |\n| foo  | bar  | foobar |\n| oof  | rab  | 2000   |\n\nThis is an interesting article: <http://test.io>\n\n## Code example\n\n```html\n<p>Test</p>\n```\n~~~\n\n## Merge two documents\n\n```python\nfrom markdownio import MarkdownIO\n\ndocument1 = MarkdownIO()\ndocument1.p("Part 1.")\n\ndocument2 = MarkdownIO()\ndocument2.p("Part 2.")\n\nfull_document = document1 + document2\nprint(full_document.output())\n```\n\noutput:\n\n```markdown\nPart 1.\n\nPart 2.\n```\n\n## Documentation\n\n- [Block elements](./documentation/block.md)\n- [Span elements](./documentation/span.md)\n',
    'author': 'u8slvn',
    'author_email': 'u8slvn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/u8slvn/markdownio',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
